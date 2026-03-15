"""Unit tests for src/enhance.py — copy, compress, and pure helpers.

Covers only non-AI code paths: no-op copy, JPEG/PNG output, droplist
filtering, and lightweight image operations (grayscale, upscale, binarize).
All AI-heavy functions (DocRes, PreP-OCR, comparison matrix) are out of scope.

Uses stdlib unittest (no external dependencies beyond OpenCV/NumPy).
Run:  python -m unittest tests.test_enhance -v
"""

import json
import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from src.enhance import (
    adaptive_binarize,
    apply_clahe,
    bilateral_denoise,
    enhance_image,
    lanczos_upscale,
    process_book,
    to_grayscale,
)


def _make_test_image(
    directory: Path, name: str = "01.png", width: int = 100, height: int = 100
) -> Path:
    """Create a synthetic colour PNG in the given directory and return its path."""
    img = np.random.randint(50, 200, (height, width, 3), dtype=np.uint8)
    path = directory / name
    cv2.imwrite(str(path), img)
    return path


# ── Pure function helpers ───────────────────────────────────────────


class TestToGrayscale(unittest.TestCase):
    def test_color_to_gray(self):
        img = np.zeros((10, 10, 3), dtype=np.uint8)
        result = to_grayscale(img)
        self.assertEqual(len(result.shape), 2)

    def test_already_gray(self):
        img = np.zeros((10, 10), dtype=np.uint8)
        result = to_grayscale(img)
        self.assertEqual(len(result.shape), 2)
        np.testing.assert_array_equal(result, img)


class TestApplyClahe(unittest.TestCase):
    def test_returns_same_shape(self):
        img = np.random.randint(0, 256, (50, 50), dtype=np.uint8)
        result = apply_clahe(img)
        self.assertEqual(result.shape, img.shape)
        self.assertEqual(result.dtype, np.uint8)


class TestBilateralDenoise(unittest.TestCase):
    def test_returns_same_shape(self):
        img = np.random.randint(0, 256, (50, 50), dtype=np.uint8)
        result = bilateral_denoise(img)
        self.assertEqual(result.shape, img.shape)


class TestAdaptiveBinarize(unittest.TestCase):
    def test_output_is_binary(self):
        img = np.random.randint(0, 256, (60, 60), dtype=np.uint8)
        result = adaptive_binarize(img)
        unique = set(np.unique(result))
        self.assertTrue(unique.issubset({0, 255}))


class TestLanczosUpscale(unittest.TestCase):
    def test_doubles_dimensions(self):
        img = np.zeros((40, 30, 3), dtype=np.uint8)
        result = lanczos_upscale(img, factor=2.0)
        self.assertEqual(result.shape[0], 80)
        self.assertEqual(result.shape[1], 60)

    def test_custom_factor(self):
        img = np.zeros((40, 30), dtype=np.uint8)
        result = lanczos_upscale(img, factor=3.0)
        self.assertEqual(result.shape[0], 120)
        self.assertEqual(result.shape[1], 90)


# ── enhance_image (no-AI flags) ────────────────────────────────────


class TestEnhanceImage(unittest.TestCase):
    def test_noop(self):
        """No flags → identity (returns the same array)."""
        img = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
        result = enhance_image(img)
        np.testing.assert_array_equal(result, img)

    def test_classical_produces_grayscale(self):
        img = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
        result = enhance_image(img, use_classical=True)
        self.assertEqual(len(result.shape), 2)  # single-channel

    def test_upscale(self):
        img = np.zeros((40, 30, 3), dtype=np.uint8)
        result = enhance_image(img, upscale=True)
        self.assertEqual(result.shape[0], 80)
        self.assertEqual(result.shape[1], 60)

    def test_binarize(self):
        img = np.random.randint(0, 256, (60, 60, 3), dtype=np.uint8)
        result = enhance_image(img, use_classical=True, binarize=True)
        unique = set(np.unique(result))
        self.assertTrue(unique.issubset({0, 255}))


# ── process_book (copy / compress) ─────────────────────────────────


class TestProcessBook(unittest.TestCase):
    def test_noop_jpg(self):
        """No enhancement flags → copies images as JPEG."""
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "input"
            out = Path(tmp) / "output"
            inp.mkdir()
            _make_test_image(inp, "01.png")
            _make_test_image(inp, "02.png")

            count = process_book(inp, out, out_format="jpg")

            self.assertEqual(count, 2)
            jpgs = sorted(out.glob("*.jpg"))
            self.assertEqual(len(jpgs), 2)
            self.assertEqual(jpgs[0].name, "01.jpg")
            self.assertEqual(jpgs[1].name, "02.jpg")

    def test_noop_png(self):
        """out_format='png' → produces .png files."""
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "input"
            out = Path(tmp) / "output"
            inp.mkdir()
            _make_test_image(inp, "01.png")

            process_book(inp, out, out_format="png")

            pngs = list(out.glob("*.png"))
            self.assertEqual(len(pngs), 1)
            self.assertEqual(pngs[0].name, "01.png")

    def test_jpeg_quality_affects_size(self):
        """Lower JPEG quality produces smaller files than higher quality."""
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "input"
            out_lo = Path(tmp) / "low"
            out_hi = Path(tmp) / "high"
            inp.mkdir()
            _make_test_image(inp, "01.png", width=200, height=200)

            process_book(inp, out_lo, out_format="jpg", jpeg_quality=10)
            process_book(inp, out_hi, out_format="jpg", jpeg_quality=95)

            lo_size = (out_lo / "01.jpg").stat().st_size
            hi_size = (out_hi / "01.jpg").stat().st_size
            self.assertGreater(hi_size, lo_size)

    def test_droplist_skips_pages(self):
        """Pages in droplist are excluded from output."""
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "pages" / "testbook"
            out = Path(tmp) / "output"
            inp.mkdir(parents=True)
            _make_test_image(inp, "01.png")
            _make_test_image(inp, "02.png")
            _make_test_image(inp, "03.png")

            # Create droplist that skips page 2
            drop_dir = Path(tmp) / "droplist" / "testbook"
            drop_dir.mkdir(parents=True)
            (drop_dir / "drop_pages.json").write_text(json.dumps([2]), encoding="utf-8")

            import src.utils as utils_mod

            orig_root = utils_mod.PROJECT_ROOT
            utils_mod.PROJECT_ROOT = Path(tmp)
            try:
                count = process_book(inp, out, out_format="png")
            finally:
                utils_mod.PROJECT_ROOT = orig_root

            self.assertEqual(count, 2)
            names = [p.name for p in sorted(out.iterdir())]
            self.assertIn("01.png", names)
            self.assertNotIn("02.png", names)
            self.assertIn("03.png", names)

    def test_empty_dir(self):
        """Empty input directory → returns 0, no crash."""
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "empty"
            out = Path(tmp) / "output"
            inp.mkdir()
            count = process_book(inp, out)
            self.assertEqual(count, 0)

    def test_returns_correct_count(self):
        """Return value matches the number of images processed."""
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "input"
            out = Path(tmp) / "output"
            inp.mkdir()
            for i in range(5):
                _make_test_image(inp, f"{i + 1:02d}.png")

            count = process_book(inp, out, out_format="png")
            self.assertEqual(count, 5)


if __name__ == "__main__":
    unittest.main()
