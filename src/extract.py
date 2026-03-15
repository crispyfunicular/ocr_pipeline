#!/usr/bin/env python3
"""
Extract each page of one or more PDFs as a PNG image (300 DPI by default).

By default, processes every PDF found in the pdfs/ directory.
Each PDF's pages are saved to pages/<pdf_stem>/.

Examples:
    python extract_pages.py                          # all PDFs in pdfs/
    python extract_pages.py pdfs/my_book.pdf         # one specific PDF
    python extract_pages.py a.pdf b.pdf --dpi 400    # two PDFs at 400 DPI
"""

import argparse
import sys
from pathlib import Path

import fitz  # PyMuPDF

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = PROJECT_ROOT / "pdfs"
PAGES_DIR = PROJECT_ROOT / "pages"


def extract_pages(
    pdf_path: Path, output_dir: Path, dpi: int = 300, book_name: str | None = None
) -> None:
    """Extract every page of a PDF as a PNG image."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load droplist if book name is known
    drop_pages: set[int] = set()
    if book_name:
        from src.utils import load_droplist

        drop_pages = load_droplist(book_name)

    doc = fitz.open(pdf_path)
    total = doc.page_count
    print(f"\n📄 {pdf_path.name}  —  {total} pages  →  {output_dir}/")
    if drop_pages:
        print(f"  ⏭️  {len(drop_pages)} pages in droplist will be skipped")

    # Zoom matrix to reach the target DPI (PDF default = 72 DPI)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    extracted = 0
    for i, page in enumerate(doc):
        page_num = i + 1
        if page_num in drop_pages:
            continue
        out_file = output_dir / f"{page_num:02d}.png"
        pix = page.get_pixmap(matrix=matrix)
        pix.save(str(out_file))
        print(
            f"  [{page_num:3d}/{total}]  {out_file.name}  ({pix.width}×{pix.height} px)"
        )
        extracted += 1

    doc.close()
    print(
        f"  ✅ {extracted} images written"
        + (f" ({total - extracted} skipped)" if drop_pages else "")
    )


def pdf_stem(pdf_path: Path) -> str:
    """Derive a clean directory name from a PDF filename."""
    # Strip common URL fragments and extensions
    stem = pdf_path.stem.split("#")[0]
    # Collapse multiple underscores
    while "__" in stem:
        stem = stem.replace("__", "_")
    return stem.strip("_")


def main(argv=None):
    """Entry point. Pass argv list for programmatic use, or None for CLI."""
    parser = argparse.ArgumentParser(
        description="Extract PDF pages as PNG images (300 DPI).",
        epilog="If no PDFs are specified, all PDFs in %(default_dir)s are processed."
        % {"default_dir": PDF_DIR},
    )
    parser.add_argument(
        "pdfs",
        nargs="*",
        type=Path,
        help=f"PDF file(s) to process. Default: all *.pdf in {PDF_DIR}/",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=PAGES_DIR,
        help=f"Parent directory for extracted pages (default: {PAGES_DIR}/)",
    )
    parser.add_argument(
        "-d",
        "--dpi",
        type=int,
        default=300,
        help="Resolution in DPI (default: 300)",
    )
    args = parser.parse_args(argv)

    # Discover PDFs
    if args.pdfs:
        pdf_files = args.pdfs
    else:
        if not PDF_DIR.is_dir():
            print(f"❌ Default PDF directory '{PDF_DIR}/' not found.", file=sys.stderr)
            print(
                f"   Place PDFs in {PDF_DIR}/ or pass them as arguments.",
                file=sys.stderr,
            )
            sys.exit(1)
        pdf_files = sorted(PDF_DIR.glob("*.pdf"))
        if not pdf_files:
            print(f"❌ No PDF files found in {PDF_DIR}/", file=sys.stderr)
            sys.exit(1)

    # Validate
    for pdf in pdf_files:
        if not pdf.exists():
            print(f"❌ File not found: {pdf}", file=sys.stderr)
            sys.exit(1)

    print(f"📚 {len(pdf_files)} PDF(s) to process at {args.dpi} DPI")

    books = []
    for pdf in pdf_files:
        stem = pdf_stem(pdf)
        out = args.output / stem
        extract_pages(pdf, out, dpi=args.dpi, book_name=stem)
        books.append(stem)

    print(f"\n🎉 Done — all pages extracted to {args.output}/")
    return books


if __name__ == "__main__":
    main()
