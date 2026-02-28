#!/usr/bin/env python3
"""
Safe image enhancement for Breton dictionary OCR pipeline.

Applies conservative, non-hallucinating enhancement to scanned book pages:
  1. (Optional) DocRes AI document restoration (--docres)
  2. Grayscale conversion
  3. CLAHE contrast equalization (makes faded ink pop)

Optionally:
  4. Bilateral denoising (--denoise, smooths paper grain but may soften text)
  5. Adaptive Gaussian thresholding (--binarize)

Default: grayscale + CLAHE only — sharpest text for VLM-based OCR.
Outputs lossless PNG.

By default, processes all subdirectories in pages/ and writes enhanced
versions to pages_enhanced/<subdir>/.

Examples:
    python enhance_pages.py                                 # all books
    python enhance_pages.py --targets le_francais_par_le_breton
    python enhance_pages.py --compare 33 --targets le_francais_par_le_breton
    python enhance_pages.py --upscale                       # with 2× Lanczos
    python enhance_pages.py --binarize                      # binary B&W output
    python enhance_pages.py --format png                    # lossless PNG
    python enhance_pages.py --docres                        # AI restoration
    python enhance_pages.py --docres --docres-task deblurring
"""

import argparse
import os
import sys
from pathlib import Path

import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = PROJECT_ROOT / "pages"
ENHANCED_DIR = PROJECT_ROOT / "pages_enhanced"
DOCRES_DIR = PROJECT_ROOT / "docres"
RESSHIFT_DIR = PROJECT_ROOT / "resshift"

from scripts.utils import discover_targets

# ── Individual processing stages ───────────────────────────────────


def to_grayscale(img: np.ndarray) -> np.ndarray:
    """Convert to grayscale. Dictionary text is B&W; color just adds noise."""
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def apply_clahe(
    img: np.ndarray, clip_limit: float = 1.5, tile_size: int = 8
) -> np.ndarray:
    """Contrast Limited Adaptive Histogram Equalization.

    Makes faded gray ink snap to high contrast against the page.
    Safe: only redistributes existing pixel intensities, never invents shapes.
    clip_limit=1.5 is conservative for already high-contrast B&W book scans.
    """
    clahe = cv2.createCLAHE(
        clipLimit=clip_limit,
        tileGridSize=(tile_size, tile_size),
    )
    return clahe.apply(img)


def bilateral_denoise(
    img: np.ndarray, d: int = 9, sigma_color: float = 75, sigma_space: float = 75
) -> np.ndarray:
    """Bilateral filter: smooths paper texture while preserving letter edges.

    Fundamentally different from Gaussian blur — it respects edge boundaries.
    """
    return cv2.bilateralFilter(img, d, sigma_color, sigma_space)


def adaptive_binarize(
    img: np.ndarray, block_size: int = 51, c_offset: int = 15
) -> np.ndarray:
    """Adaptive Gaussian thresholding — computes threshold per local region.

    Unlike global Otsu, this handles uneven illumination and binding/gutter
    shadows gracefully because each pixel neighborhood gets its own threshold.

    block_size: size of the local neighborhood (must be odd). Larger values
                are more tolerant of gradual illumination changes.
    c_offset:   constant subtracted from the local mean. Higher values make
                the threshold more lenient (more white, less noise).
    """
    return cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size,
        c_offset,
    )


def morphological_cleanup(img: np.ndarray, kernel_size: int = 2) -> np.ndarray:
    """Close small gaps in letter strokes caused by thresholding.

    Uses a tiny kernel so it only fills 1-2px breaks without merging letters.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)


def lanczos_upscale(img: np.ndarray, factor: float = 2.0) -> np.ndarray:
    """Scale up using Lanczos4 interpolation — mathematically safe, no hallucination."""
    return cv2.resize(img, None, fx=factor, fy=factor, interpolation=cv2.INTER_LANCZOS4)


# ── DocRes AI restoration ──────────────────────────────────────────

_docres_model = None  # lazily loaded


def _load_docres(model_path: str) -> object:
    """Load the DocRes Restormer model (lazy, cached)."""
    global _docres_model
    if _docres_model is not None:
        return _docres_model

    # Workaround: WSL2 NVIDIA stub libcuda.so.1 contains a non-UTF-8 byte
    # that makes ctypes.CDLL fail with UnicodeDecodeError. Pre-loading the
    # unversioned .so avoids the bug and lets PyTorch discover CUDA.
    import ctypes, ctypes.util
    if ctypes.util.find_library("cuda"):
        try:
            ctypes.cdll.LoadLibrary("/usr/lib/wsl/lib/libcuda.so")
        except OSError:
            pass  # not WSL or path doesn't exist — harmless

    import torch

    # Add DocRes to path so its modules can be imported
    docres_root = str(DOCRES_DIR.resolve())
    if docres_root not in sys.path:
        sys.path.insert(0, docres_root)

    from utils import convert_state_dict
    from models import restormer_arch

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  🧠 Loading DocRes model on {device}...")

    model = restormer_arch.Restormer(
        inp_channels=6,
        out_channels=3,
        dim=48,
        num_blocks=[2, 3, 3, 4],
        num_refinement_blocks=4,
        heads=[1, 2, 4, 8],
        ffn_expansion_factor=2.66,
        bias=False,
        LayerNorm_type="WithBias",
        dual_pixel_task=True,
    )

    state = convert_state_dict(
        torch.load(model_path, map_location=device)["model_state"]
    )
    model.load_state_dict(state)
    model.eval()
    model = model.to(device)
    _docres_model = model
    return model


def _stride_integral(img: np.ndarray, stride: int = 8):
    """Pad image so dimensions are multiples of stride. Returns (padded, pad_h, pad_w)."""
    h, w = img.shape[:2]
    pad_h = (stride - h % stride) % stride
    pad_w = (stride - w % stride) % stride
    if pad_h > 0 or pad_w > 0:
        padded = cv2.copyMakeBorder(img, pad_h, 0, pad_w, 0, cv2.BORDER_REFLECT_101)
    else:
        padded = img
    return padded, pad_h, pad_w


# Default task chain: deshadow first (normalize lighting), then deblur
# (sharpen text), then appearance (final background cleanup).
DEFAULT_DOCRES_TASKS = ["deshadowing", "deblurring", "appearance"]


def docres_restore(
    img: np.ndarray, task: str = "appearance", model_path: str | None = None
) -> np.ndarray:
    """Apply a single DocRes AI document restoration task.

    Supported tasks: deshadowing, deblurring, appearance.
    The model removes shadows, deblurs text, or enhances appearance
    using a Restormer architecture with Dynamic Task-Specific Prompts.
    """
    import torch

    if model_path is None:
        model_path = str(DOCRES_DIR / "checkpoints" / "docres.pkl")

    model = _load_docres(model_path)
    device = next(model.parameters()).device
    MAX_SIZE = 1600

    h, w = img.shape[:2]

    if task == "deshadowing":
        # Deshadow prompt: estimate background illumination
        resized = cv2.resize(img, (1024, 1024))
        rgb_planes = cv2.split(resized)
        bg_imgs = []
        for plane in rgb_planes:
            dilated = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg = cv2.medianBlur(dilated, 21)
            bg_imgs.append(bg)
        prompt = cv2.merge(bg_imgs)
        prompt = cv2.resize(prompt, (w, h))

    elif task == "deblurring":
        # Deblur prompt: high-frequency edges via Sobel
        if max(w, h) >= MAX_SIZE:
            in_img = cv2.resize(img, (MAX_SIZE, MAX_SIZE))
        else:
            in_img = img
        in_img, pad_h, pad_w = _stride_integral(in_img, 8)
        sx = cv2.Sobel(in_img, cv2.CV_16S, 1, 0)
        sy = cv2.Sobel(in_img, cv2.CV_16S, 0, 1)
        prompt = cv2.addWeighted(
            cv2.convertScaleAbs(sx), 0.5, cv2.convertScaleAbs(sy), 0.5, 0
        )
        prompt = cv2.cvtColor(
            cv2.cvtColor(prompt, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR
        )

        combined = np.concatenate((in_img, prompt), -1) / 255.0
        tensor = (
            torch.from_numpy(combined.transpose(2, 0, 1)).unsqueeze(0).half().to(device)
        )
        model_h = model.half()
        with torch.no_grad():
            pred = model_h(tensor)
            pred = torch.clamp(pred, 0, 1)
            pred = pred[0].permute(1, 2, 0).cpu().numpy()
            out = (pred * 255).astype(np.uint8)
            out = out[pad_h:, pad_w:]
            if max(w, h) >= MAX_SIZE:
                out = cv2.resize(out, (w, h))
            return out

    elif task == "appearance":
        # Appearance prompt: background estimation via dilation + median
        resized = cv2.resize(img, (1024, 1024))
        rgb_planes = cv2.split(resized)
        result_norm_planes = []
        for plane in rgb_planes:
            dilated = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg = cv2.medianBlur(dilated, 21)
            diff = 255 - cv2.absdiff(plane, bg)
            norm = cv2.normalize(
                diff,
                None,
                alpha=0,
                beta=255,
                norm_type=cv2.NORM_MINMAX,
                dtype=cv2.CV_8UC1,
            )
            result_norm_planes.append(norm)
        prompt = cv2.merge(result_norm_planes)
        prompt = cv2.resize(prompt, (w, h))

    else:
        raise ValueError(
            f"Unsupported DocRes task: {task}. "
            f"Use: deshadowing, deblurring, appearance"
        )

    # Common inference path for deshadowing / appearance
    combined = np.concatenate((img, prompt), -1)
    if max(w, h) < MAX_SIZE:
        combined, pad_h, pad_w = _stride_integral(combined, 8)
    else:
        combined = cv2.resize(combined, (MAX_SIZE, MAX_SIZE))

    tensor = (
        torch.from_numpy(combined.transpose(2, 0, 1) / 255.0)
        .unsqueeze(0)
        .half()
        .to(device)
    )
    model_h = model.half()

    with torch.no_grad():
        pred = model_h(tensor)
        pred = torch.clamp(pred, 0, 1)
        pred = pred[0].permute(1, 2, 0).cpu().numpy()
        pred = (pred * 255).astype(np.uint8)

        if max(w, h) < MAX_SIZE:
            return pred[pad_h:, pad_w:]
        else:
            pred[pred == 0] = 1
            shadow_map = cv2.resize(img, (MAX_SIZE, MAX_SIZE)).astype(
                float
            ) / pred.astype(float)
            shadow_map = cv2.resize(shadow_map, (w, h))
            shadow_map[shadow_map == 0] = 0.00001
            return np.clip(img.astype(float) / shadow_map, 0, 255).astype(np.uint8)


# ── PreP-OCR / ResShift deblurring ─────────────────────────────────

_resshift_sampler = None


def _load_resshift_sampler():
    """Lazy-load the ResShift sampler (cached)."""
    global _resshift_sampler
    if _resshift_sampler is not None:
        return _resshift_sampler

    import sys
    import torch
    from omegaconf import OmegaConf

    # ResShift has a 'utils/' package that conflicts with DocRes's 'utils.py'.
    # Temporarily remove DocRes from sys.path during ResShift loading.
    docres_path = str(DOCRES_DIR.resolve())
    docres_was_in_path = docres_path in sys.path
    if docres_was_in_path:
        sys.path.remove(docres_path)

    # Also remove any cached 'utils' module from DocRes
    cached_utils = {}
    for key in list(sys.modules.keys()):
        if key == "utils" or key.startswith("utils."):
            cached_utils[key] = sys.modules.pop(key)

    # Add ResShift to Python path so its internal imports work
    resshift_path = str(RESSHIFT_DIR)
    if resshift_path not in sys.path:
        sys.path.insert(0, resshift_path)

    config_path = RESSHIFT_DIR / "configs" / "deblur_prepocr.yaml"
    if not config_path.exists():
        raise FileNotFoundError(
            f"ResShift config not found: {config_path}\n"
            "  Run ./setup.sh to set up ResShift/PreP-OCR."
        )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"  🧠 Loading ResShift/PreP-OCR model on {device}...")

    configs = OmegaConf.load(str(config_path))

    from sampler import ResShiftSampler
    sampler = ResShiftSampler(
        configs,
        sf=1,
        chop_size=256,
        chop_stride=256,
        chop_bs=1,
        use_amp=True,
        seed=12345,
    )

    # Restore DocRes path (needed if DocRes runs again later)
    if docres_was_in_path and docres_path not in sys.path:
        sys.path.append(docres_path)

    _resshift_sampler = sampler
    return sampler


def prepocr_restore(img: np.ndarray) -> np.ndarray:
    """Apply PreP-OCR ResShift diffusion deblurring.

    Processes the image in tiles (256×256) so it works at any resolution.
    Returns a deblurred BGR numpy uint8 image.
    """
    import torch
    from contextlib import nullcontext

    sampler = _load_resshift_sampler()

    # BGR → RGB, uint8 → float32 [0, 1]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0

    # HWC → 1CHW tensor on GPU
    tensor = torch.from_numpy(rgb.transpose(2, 0, 1)).unsqueeze(0).cuda()

    # Normalize to [-1, 1]
    tensor_norm = (tensor - 0.5) / 0.5

    context = torch.cuda.amp.autocast if sampler.use_amp else nullcontext

    # Tiled inference (mirrors ResShift's _process_per_image)
    with torch.no_grad():
        if tensor_norm.shape[2] > sampler.chop_size or tensor_norm.shape[3] > sampler.chop_size:
            from utils.util_image import ImageSpliterTh
            spliter = ImageSpliterTh(
                tensor_norm,
                sampler.chop_size,
                stride=sampler.chop_stride,
                sf=sampler.sf,
                extra_bs=sampler.chop_bs,
            )
            for lq_patch, index_infos in spliter:
                with context():
                    sr_patch = sampler.sample_func(
                        lq_patch,
                        noise_repeat=False,
                        mask=None,
                    )
                spliter.update(sr_patch, index_infos)
            result = spliter.gather()
        else:
            with context():
                result = sampler.sample_func(
                    tensor_norm,
                    noise_repeat=False,
                    mask=None,
                )

    # sample_func returns [-1, 1], denormalize to [0, 1]
    result = result * 0.5 + 0.5
    result = result.clamp(0, 1)

    # 1CHW → HWC, float → uint8, RGB → BGR
    out = result[0].permute(1, 2, 0).cpu().numpy()
    out = (out * 255).astype(np.uint8)
    out = cv2.cvtColor(out, cv2.COLOR_RGB2BGR)

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return out


# ── Comparison matrix ──────────────────────────────────────────────


def run_comparison(
    img: np.ndarray,
    book: str,
    page: str,
    out_root: Path,
    docres_model: str | None = None,
) -> Path:
    """Generate all permutations of enhancement steps for comparison.

    Saves 18 images to out_root/compare/<book>/<page>/:
    - 3 individual DocRes sub-steps
    - 3 individual main steps
    - 6 two-step permutations
    - 6 three-step permutations
    """
    import torch

    out_dir = out_root / "compare" / book / page
    out_dir.mkdir(parents=True, exist_ok=True)

    def _save(name: str, result: np.ndarray):
        path = out_dir / f"{name}.png"
        cv2.imwrite(str(path), result)
        size_kb = path.stat().st_size / 1024
        print(f"    ✅ {name}.png  ({result.shape[1]}×{result.shape[0]} px, {size_kb:.0f} KB)")

    def _clear():
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # ── Define atomic steps ─────────────────────────────────

    def step_docres_pipeline(x: np.ndarray) -> np.ndarray:
        """Full DocRes chain: deshadowing → deblurring → appearance."""
        r = x
        for task in DEFAULT_DOCRES_TASKS:
            r = docres_restore(r, task=task, model_path=docres_model)
            _clear()
        return r

    def step_prepocr(x: np.ndarray) -> np.ndarray:
        """ResShift diffusion deblurring."""
        r = prepocr_restore(x)
        _clear()
        return r

    def step_classical(x: np.ndarray) -> np.ndarray:
        """Grayscale + CLAHE. Returns 3-channel BGR for chaining."""
        r = to_grayscale(x)
        r = apply_clahe(r)
        # Convert back to BGR so other steps can process it
        if len(r.shape) == 2:
            r = cv2.cvtColor(r, cv2.COLOR_GRAY2BGR)
        return r

    STEPS = {
        "docres_pipeline": step_docres_pipeline,
        "prepocr": step_prepocr,
        "classical": step_classical,
    }

    # ── Save original ───────────────────────────────────────
    _save("original", img)

    # ── Phase 0: Individual DocRes sub-steps ────────────────
    print("  📊 Phase 0/4: Individual DocRes sub-steps")
    for task in DEFAULT_DOCRES_TASKS:
        result = docres_restore(img, task=task, model_path=docres_model)
        _clear()
        _save(f"docres_{task}", result)

    # ── Phase 1: Individual main steps ──────────────────────
    print("  📊 Phase 1/4: Individual steps")
    singles = {}
    for name, fn in STEPS.items():
        result = fn(img)
        singles[name] = result
        _save(name, result)

    # ── Phase 2: Two-step permutations ──────────────────────
    print("  📊 Phase 2/4: Two-step permutations")
    step_names = list(STEPS.keys())
    doubles = {}
    for first in step_names:
        for second in step_names:
            if first == second:
                continue
            combo_name = f"{first}-{second}"
            result = STEPS[second](singles[first])
            doubles[combo_name] = result
            _save(combo_name, result)

    # ── Phase 3: Three-step permutations ────────────────────
    print("  📊 Phase 3/4: Three-step permutations")
    for first in step_names:
        for second in step_names:
            if second == first:
                continue
            third = [s for s in step_names if s != first and s != second][0]
            combo_name = f"{first}-{second}-{third}"
            two_step_key = f"{first}-{second}"
            result = STEPS[third](doubles[two_step_key])
            _save(combo_name, result)

    print(f"  📁 All comparisons saved to {out_dir}/")
    return out_dir


# ── Full pipeline ──────────────────────────────────────────────────


def enhance_image(
    img: np.ndarray,
    upscale: bool = False,
    binarize: bool = False,
    denoise: bool = False,
    clip_limit: float = 1.5,
    block_size: int = 51,
    c_offset: int = 15,
    use_docres: bool = False,
    docres_tasks: list[str] | None = None,
    docres_model: str | None = None,
    use_prepocr: bool = True,
) -> np.ndarray:
    """Apply the full enhancement pipeline.

    Default: grayscale + CLAHE only — improves contrast while keeping
    text perfectly sharp for VLM-based OCR.

    Optional AI enhancements (run before classical processing):
    - DocRes: deshadowing → deblurring → appearance (--no-docres to disable)
    - PreP-OCR: ResShift diffusion deblurring (--no-prepocr to disable)
    """
    result = img
    if use_docres:
        import torch
        tasks = docres_tasks or DEFAULT_DOCRES_TASKS
        for i, task in enumerate(tasks):
            result = docres_restore(result, task=task, model_path=docres_model)
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    if use_prepocr:
        result = prepocr_restore(result)
    result = to_grayscale(result)
    result = apply_clahe(result, clip_limit=clip_limit)
    if denoise:
        result = bilateral_denoise(result)
    if binarize:
        result = adaptive_binarize(result, block_size=block_size, c_offset=c_offset)
        result = morphological_cleanup(result)
    if upscale:
        result = lanczos_upscale(result)
    return result


# ── Comparison image ───────────────────────────────────────────────


def make_comparison(
    original: np.ndarray, enhanced: np.ndarray, output_path: Path
) -> None:
    """Save a side-by-side before/after comparison image."""
    # Ensure same dimensions for comparison
    if len(original.shape) == 3:
        original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    else:
        original_gray = original

    # Resize enhanced to match original height if upscaled
    if original_gray.shape != enhanced.shape:
        enhanced_resized = cv2.resize(
            enhanced,
            (original_gray.shape[1], original_gray.shape[0]),
            interpolation=cv2.INTER_AREA,
        )
    else:
        enhanced_resized = enhanced

    # Add labels
    h, w = original_gray.shape
    label_h = 60
    canvas_h = h + label_h

    # Create side-by-side canvas
    separator_w = 4
    canvas = np.ones((canvas_h, w * 2 + separator_w), dtype=np.uint8) * 200

    # Draw labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(canvas, "ORIGINAL", (w // 3, 40), font, 1.2, (0,), 3)
    cv2.putText(canvas, "ENHANCED", (w + separator_w + w // 3, 40), font, 1.2, (0,), 3)

    # Draw images
    canvas[label_h : label_h + h, :w] = original_gray
    canvas[label_h : label_h + h, w + separator_w :] = enhanced_resized

    # Draw separator
    canvas[label_h:, w : w + separator_w] = 128

    cv2.imwrite(str(output_path), canvas)


# ── Batch processing ──────────────────────────────────────────────


def process_book(
    input_dir: Path,
    output_dir: Path,
    upscale: bool = False,
    binarize: bool = False,
    denoise: bool = False,
    compare_page: int | None = None,
    clip_limit: float = 1.5,
    block_size: int = 51,
    c_offset: int = 15,
    out_format: str = "jpg",
    jpeg_quality: int = 85,
    use_docres: bool = False,
    docres_tasks: list[str] | None = None,
    docres_model: str | None = None,
    use_prepocr: bool = True,
) -> int:
    """Process all pages of a single book directory. Returns count."""
    output_dir.mkdir(parents=True, exist_ok=True)
    images = sorted(input_dir.glob("*.png"))

    if not images:
        print(f"  ⚠️  No PNG files in {input_dir}/")
        return 0

    print(f"\n📖 {input_dir.name}  —  {len(images)} pages")

    for i, img_path in enumerate(images, 1):
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"  ⚠️  Could not read {img_path.name}, skipping")
            continue

        enhanced = enhance_image(
            img,
            upscale=upscale,
            binarize=binarize,
            denoise=denoise,
            clip_limit=clip_limit,
            block_size=block_size,
            c_offset=c_offset,
            use_docres=use_docres,
            docres_tasks=docres_tasks,
            docres_model=docres_model,
            use_prepocr=use_prepocr,
        )

        ext = "png" if out_format == "png" else "jpg"
        out_path = output_dir / f"{img_path.stem}.{ext}"
        if ext == "jpg":
            cv2.imwrite(
                str(out_path), enhanced, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]
            )
        else:
            cv2.imwrite(str(out_path), enhanced)

        # Print progress for every page
        size_kb = out_path.stat().st_size / 1024
        print(
            f"  [{i:3d}/{len(images)}]  {out_path.name}"
            f"  ({enhanced.shape[1]}×{enhanced.shape[0]} px, {size_kb:.0f} KB)"
        )

        # Generate comparison if requested
        page_num = int(img_path.stem) if img_path.stem.isdigit() else None
        if compare_page is not None and page_num == compare_page:
            comp_path = output_dir / f"compare_{compare_page:02d}.png"
            make_comparison(img, enhanced, comp_path)
            print(f"  📊 Comparison saved: {comp_path}")

    print(f"  ✅ {len(images)} pages enhanced → {output_dir}/")
    return len(images)


def main(argv=None):
    """Entry point. Pass argv list for programmatic use, or None for CLI."""
    parser = argparse.ArgumentParser(
        description="Safe image enhancement for Breton dictionary OCR.",
        epilog="Processes pages/<book>/ → pages_enhanced/<book>/",
    )
    parser.add_argument(
        "--targets",
        nargs="*",
        help=f"Book folder name(s) under {PAGES_DIR}/ or individual image file path(s). "
        f"Default: all subdirectories.",
    )
    parser.add_argument(
        "-i",
        "--input-dir",
        type=Path,
        default=PAGES_DIR,
        help=f"Parent directory containing book subdirs (default: {PAGES_DIR}/)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=ENHANCED_DIR,
        help=f"Parent directory for enhanced output (default: {ENHANCED_DIR}/)",
    )
    parser.add_argument(
        "--upscale",
        action="store_true",
        help="Apply 2× Lanczos upscale (safe, useful for small text)",
    )
    parser.add_argument(
        "--binarize",
        action="store_true",
        help="Apply adaptive binarization (B&W output). Default: off (grayscale)",
    )
    parser.add_argument(
        "--no-denoise",
        dest="denoise",
        action="store_false",
        default=True,
        help="Disable bilateral denoising (on by default)",
    )
    parser.add_argument(
        "--format",
        choices=["jpg", "png"],
        default="png",
        help="Output format (default: png — lossless, best quality for OCR)",
    )
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=85,
        help="JPEG quality 0-100 (default: 85, good balance for text scans)",
    )
    parser.add_argument(
        "--compare",
        type=int,
        metavar="PAGE",
        help="Generate a side-by-side comparison image for page N",
    )
    parser.add_argument(
        "--clip-limit",
        type=float,
        default=1.5,
        help="CLAHE clip limit (default: 1.5, higher = more contrast)",
    )
    parser.add_argument(
        "--block-size",
        type=int,
        default=51,
        help="Adaptive threshold block size in px (default: 51, must be odd)",
    )
    parser.add_argument(
        "--c-offset",
        type=int,
        default=15,
        help="Adaptive threshold offset (default: 15, higher = more white)",
    )
    parser.add_argument(
        "--no-docres",
        dest="docres",
        action="store_false",
        default=True,
        help="Disable DocRes AI document restoration (on by default)",
    )
    parser.add_argument(
        "--docres-tasks",
        nargs="+",
        choices=["deshadowing", "deblurring", "appearance"],
        default=None,
        help="DocRes tasks to run, in order (default: deshadowing deblurring appearance)",
    )
    parser.add_argument(
        "--docres-model",
        type=str,
        default=None,
        help="Path to docres.pkl weights (default: ./docres/checkpoints/docres.pkl)",
    )
    parser.add_argument(
        "--no-prepocr",
        dest="prepocr",
        action="store_false",
        default=True,
        help="Disable PreP-OCR ResShift diffusion deblurring (on by default)",
    )
    args = parser.parse_args(argv)

    # Validate DocRes setup
    if args.docres:
        model_path = args.docres_model or str(DOCRES_DIR / "checkpoints" / "docres.pkl")
        if not Path(model_path).exists():
            print(f"❌ DocRes weights not found: {model_path}", file=sys.stderr)
            print(
                f"   Download from: https://huggingface.co/DaVinciCode/doctra-docres-main",
                file=sys.stderr,
            )
            sys.exit(1)

    book_dirs, single_images = discover_targets(args.targets, args.input_dir)
    if not book_dirs and not single_images:
        print(f"❌ No targets found in {args.input_dir}/", file=sys.stderr)
        sys.exit(1)

    if book_dirs:
        print(f"🔧 Enhancing {len(book_dirs)} book(s)")
    if single_images:
        print(f"🔧 Enhancing {len(single_images)} individual image(s)")
    print(
        f"  📦 Output: {args.format.upper()}"
        f"{f' (q={args.jpeg_quality})' if args.format == 'jpg' else ''}"
    )
    if args.docres:
        tasks = args.docres_tasks or DEFAULT_DOCRES_TASKS
        print(f"  🧠 DocRes AI restoration enabled (tasks: {' → '.join(tasks)})")
    if args.prepocr:
        print("  🧠 PreP-OCR ResShift deblurring enabled")
    if args.upscale:
        print("  ↗️  2× Lanczos upscale enabled")
    if args.binarize:
        print("  ⬛ Binarization enabled (adaptive Gaussian)")
    if args.compare is not None:
        print(f"  📊 Comparison will be generated for page {args.compare}")

    total = 0
    books_processed = []

    # Process full book directories
    for book_dir in book_dirs:
        out_dir = args.output / book_dir.name
        count = process_book(
            book_dir,
            out_dir,
            upscale=args.upscale,
            binarize=args.binarize,
            denoise=args.denoise,
            compare_page=args.compare,
            clip_limit=args.clip_limit,
            block_size=args.block_size,
            c_offset=args.c_offset,
            out_format=args.format,
            jpeg_quality=args.jpeg_quality,
            use_docres=args.docres,
            docres_tasks=args.docres_tasks,
            docres_model=args.docres_model,
            use_prepocr=args.prepocr,
        )
        total += count
        books_processed.append(book_dir.name)

    # Process individual images
    for img_path in single_images:
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"  ⚠️  Could not read {img_path}, skipping")
            continue

        enhanced = enhance_image(
            img,
            upscale=args.upscale,
            binarize=args.binarize,
            denoise=args.denoise,
            clip_limit=args.clip_limit,
            block_size=args.block_size,
            c_offset=args.c_offset,
            use_docres=args.docres,
            docres_tasks=args.docres_tasks,
            docres_model=args.docres_model,
            use_prepocr=args.prepocr,
        )

        # Output to pages_enhanced/<book>/<page>.ext (mirrors book-level behavior)
        ext = "png" if args.format == "png" else "jpg"
        book_name = img_path.parent.name
        out_dir = PROJECT_ROOT / "pages_enhanced" / book_name
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{img_path.stem}.{ext}"
        if ext == "jpg":
            cv2.imwrite(
                str(out_path), enhanced, [cv2.IMWRITE_JPEG_QUALITY, args.jpeg_quality]
            )
        else:
            cv2.imwrite(str(out_path), enhanced)

        size_kb = out_path.stat().st_size / 1024
        rel_out = out_path.relative_to(PROJECT_ROOT)
        print(
            f"  ✅ {img_path} → {rel_out}"
            f"  ({enhanced.shape[1]}×{enhanced.shape[0]} px, {size_kb:.0f} KB)"
        )
        total += 1

    print(f"\n🎉 Done — {total} pages enhanced")
    return books_processed


if __name__ == "__main__":
    main()
