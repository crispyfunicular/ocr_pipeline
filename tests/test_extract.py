"""Unit tests for src/extract.py — PDF extraction and helpers.

Uses stdlib unittest (no external dependencies beyond PyMuPDF).
Run:  python -m unittest tests.test_extract -v
"""

import json
import tempfile
import unittest
from pathlib import Path

import fitz  # PyMuPDF

from src.extract import extract_pages, main, pdf_stem


def _make_tiny_pdf(path: Path, pages: int = 2) -> None:
    """Create a minimal valid PDF with coloured rectangles so pages aren't blank."""
    doc = fitz.open()
    colours = [fitz.pdfcolor["red"], fitz.pdfcolor["blue"], fitz.pdfcolor["green"]]
    for i in range(pages):
        page = doc.new_page(width=72, height=72)  # 1 inch square at 72 DPI
        # Draw a filled rectangle so the page has visible content
        rect = fitz.Rect(10, 10, 62, 62)
        page.draw_rect(
            rect, color=colours[i % len(colours)], fill=colours[i % len(colours)]
        )
    doc.save(str(path))
    doc.close()


# ── pdf_stem ────────────────────────────────────────────────────────


class TestPdfStem(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(pdf_stem(Path("my_book.pdf")), "my_book")

    def test_url_fragment(self):
        self.assertEqual(pdf_stem(Path("my_book#page=3.pdf")), "my_book")

    def test_double_underscores(self):
        self.assertEqual(pdf_stem(Path("my__book__.pdf")), "my_book")

    def test_leading_trailing_underscores(self):
        self.assertEqual(pdf_stem(Path("_hello_.pdf")), "hello")


# ── extract_pages ───────────────────────────────────────────────────


class TestExtractPages(unittest.TestCase):
    def test_basic_extraction(self):
        """Extracts a 2-page PDF into 2 PNGs with correct filenames."""
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "book.pdf"
            out = Path(tmp) / "output"
            _make_tiny_pdf(pdf, pages=2)

            extract_pages(pdf, out, dpi=72)

            pngs = sorted(out.glob("*.png"))
            self.assertEqual(len(pngs), 2)
            self.assertEqual(pngs[0].name, "01.png")
            self.assertEqual(pngs[1].name, "02.png")
            # Files should be non-empty
            for p in pngs:
                self.assertGreater(p.stat().st_size, 0)

    def test_custom_dpi(self):
        """Higher DPI produces larger images."""
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "book.pdf"
            out_lo = Path(tmp) / "lo"
            out_hi = Path(tmp) / "hi"
            _make_tiny_pdf(pdf, pages=1)

            extract_pages(pdf, out_lo, dpi=72)
            extract_pages(pdf, out_hi, dpi=300)

            lo_size = (out_lo / "01.png").stat().st_size
            hi_size = (out_hi / "01.png").stat().st_size
            self.assertGreater(hi_size, lo_size)

    def test_droplist_skips_pages(self):
        """Pages in drop_pages.json are skipped during extraction."""
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "book.pdf"
            out = Path(tmp) / "output"
            _make_tiny_pdf(pdf, pages=3)

            # Create a droplist that skips page 2
            drop_dir = Path(tmp) / "droplist" / "testbook"
            drop_dir.mkdir(parents=True)
            (drop_dir / "drop_pages.json").write_text(json.dumps([2]), encoding="utf-8")

            # Monkey-patch PROJECT_ROOT so load_droplist finds our temp droplist
            import src.utils as utils_mod

            orig_root = utils_mod.PROJECT_ROOT
            utils_mod.PROJECT_ROOT = Path(tmp)
            try:
                extract_pages(pdf, out, dpi=72, book_name="testbook")
            finally:
                utils_mod.PROJECT_ROOT = orig_root

            pngs = sorted(out.glob("*.png"))
            names = [p.name for p in pngs]
            self.assertIn("01.png", names)
            self.assertNotIn("02.png", names)
            self.assertIn("03.png", names)
            self.assertEqual(len(pngs), 2)


# ── main() CLI ──────────────────────────────────────────────────────


class TestExtractMain(unittest.TestCase):
    def test_missing_pdf_exits(self):
        """Passing a nonexistent PDF path causes SystemExit."""
        with self.assertRaises(SystemExit):
            main(["nonexistent_file.pdf"])

    def test_explicit_pdf(self):
        """main() with an explicit PDF returns list of book stems."""
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "my_book.pdf"
            out = Path(tmp) / "pages"
            _make_tiny_pdf(pdf, pages=1)

            books = main([str(pdf), "-o", str(out)])

            self.assertEqual(books, ["my_book"])
            self.assertTrue((out / "my_book" / "01.png").exists())


if __name__ == "__main__":
    unittest.main()
