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
) -> np.ndarray:
    """Apply the full enhancement pipeline.

    Default: grayscale + CLAHE only — improves contrast while keeping
    text perfectly sharp for VLM-based OCR.

    When DocRes is enabled, chains the requested tasks sequentially
    (default: deshadowing → deblurring → appearance).
    """
    result = img
    if use_docres:
        import torch
        tasks = docres_tasks or DEFAULT_DOCRES_TASKS
        for i, task in enumerate(tasks):
            result = docres_restore(result, task=task, model_path=docres_model)
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
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
        )

        # Output next to original with _enhanced suffix
        ext = "png" if args.format == "png" else "jpg"
        out_path = img_path.parent / f"{img_path.stem}_enhanced.{ext}"
        if ext == "jpg":
            cv2.imwrite(
                str(out_path), enhanced, [cv2.IMWRITE_JPEG_QUALITY, args.jpeg_quality]
            )
        else:
            cv2.imwrite(str(out_path), enhanced)

        size_kb = out_path.stat().st_size / 1024
        print(
            f"  ✅ {img_path.name} → {out_path.name}"
            f"  ({enhanced.shape[1]}×{enhanced.shape[0]} px, {size_kb:.0f} KB)"
        )
        total += 1

    print(f"\n🎉 Done — {total} pages enhanced")
    return books_processed


if __name__ == "__main__":
    main()
