#!/usr/bin/env python3
"""
Unified OCR pipeline CLI for Breton-French corpus extraction.

Stages:
    extract   — PDF → PNG pages (300 DPI)
    enhance   — Image enhancement (CLAHE + optional DocRes AI)
    ocr       — VLM-based bilingual text extraction (OpenAI / Anthropic)
    review    — JSONL quality assurance
    evaluate  — Compute WER and CER against human reference
    corpus    — Deduplicate and merge review output into corpus/<book>.jsonl
    ignore    — Add pages to the per-book droplist
    run       — Chain all stages end-to-end


Usage:
    python pipeline.py run                          # full pipeline, all PDFs
    python pipeline.py run pdfs/my_book.pdf         # full pipeline, one PDF
    python pipeline.py extract                      # extract only, all PDFs
    python pipeline.py enhance --docres --prepocr      # enhance with AI
    python pipeline.py ocr Manuel_1865             # OCR one book
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def cmd_extract(args):
    """Extract pages from PDFs."""
    from scripts.extract import main as extract_main

    argv = list(args.targets) if args.targets else []
    if args.dpi:
        argv.extend(["--dpi", str(args.dpi)])
    return extract_main(argv)


def cmd_enhance(args):
    """Enhance extracted pages."""
    from scripts.enhance import main as enhance_main

    argv = []
    if args.targets:
        argv.extend(["--targets"] + list(args.targets))
    if args.docres:
        argv.append("--docres")
    if args.docres_tasks:
        argv.extend(["--docres-tasks"] + list(args.docres_tasks))
    if args.prepocr:
        argv.append("--prepocr")
    if args.classical:
        argv.append("--classical")
    return enhance_main(argv)


def cmd_compare(args):
    """Generate comparison matrix of all enhancement permutations."""
    from pathlib import Path
    from scripts.enhance import run_comparison, PROJECT_ROOT
    import cv2

    img_path = Path(args.image)
    if not img_path.exists():
        print(f"❌ Image not found: {img_path}", file=sys.stderr)
        sys.exit(1)

    img = cv2.imread(str(img_path))
    if img is None:
        print(f"❌ Could not read image: {img_path}", file=sys.stderr)
        sys.exit(1)

    # Infer book and page from path: pages/<book>/<page>.png
    img_path = img_path.resolve()
    page = img_path.stem
    book = img_path.parent.name

    print(f"📊 Generating comparison matrix for {book}/{page}")
    print(f"  Image: {img.shape[1]}×{img.shape[0]} px")

    run_comparison(
        img,
        book=book,
        page=page,
        out_root=PROJECT_ROOT,
    )

    print(f"\n🎉 Done — see compare/{book}/{page}/")


def cmd_ocr(args):
    """Run OCR extraction."""
    from scripts.ocr import main as ocr_main

    argv = []
    if args.targets:
        argv.extend(["--targets"] + list(args.targets))
    if args.model:
        argv.extend(["--model", args.model])
    if args.output:
        argv.extend(["--output", str(args.output)])
    if args.debug:
        argv.append("--debug")
    if args.limit:
        argv.extend(["--limit", str(args.limit)])
    return ocr_main(argv)


def cmd_review(args):
    """Copy OCR output to review/ and run quality assurance."""
    from scripts.review import main as review_main

    argv = []
    if args.targets:
        argv.extend(list(args.targets))
    if args.model:
        argv.extend(["--model", args.model])
    if args.yes:
        argv.append("--yes")
    return review_main(argv)


def cmd_evaluate(args):
    """Run evaluation (WER/CER)."""
    from scripts.evaluate import main as evaluate_main

    argv = []
    if args.targets:
        argv.extend(list(args.targets))
    return evaluate_main(argv)


def cmd_corpus(args):
    """Build corpus from reviewed output."""
    from scripts.corpus import main as corpus_main

    argv = []
    if args.targets:
        argv.extend(["--targets"] + list(args.targets))
    if args.output:
        argv.extend(["--output", str(args.output)])
    return corpus_main(argv)


def cmd_ignore(args):
    """Add pages to the per-book droplist."""
    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".tif"}

    for image in args.images:
        img_path = Path(image).resolve()

        # Validate file
        if not img_path.exists():
            print(f"❌ File not found: {image}", file=sys.stderr)
            sys.exit(1)
        if img_path.suffix.lower() not in IMAGE_EXTENSIONS:
            print(f"❌ Not an image file: {image}", file=sys.stderr)
            sys.exit(1)

        # Extract book name and page number from path
        book = img_path.parent.name
        try:
            page_num = int(img_path.stem)
        except ValueError:
            print(
                f"❌ Cannot parse page number from filename: {img_path.name}",
                file=sys.stderr,
            )
            sys.exit(1)

        # Load or create droplist
        drop_dir = PROJECT_ROOT / "droplist" / book
        drop_file = drop_dir / "drop_pages.json"

        if drop_file.exists():
            data = json.loads(drop_file.read_text(encoding="utf-8"))
            pages = set(data)
        else:
            pages = set()

        if page_num in pages:
            print(f"  ⏭️  {book} page {page_num} — already in droplist")
            continue

        pages.add(page_num)
        drop_dir.mkdir(parents=True, exist_ok=True)
        drop_file.write_text(
            json.dumps(sorted(pages), indent=4) + "\n", encoding="utf-8"
        )
        print(f"  ✅ {book} page {page_num} — added to droplist")


def cmd_run(args):
    """Run the full pipeline end-to-end."""
    from scripts.extract import main as extract_main
    from scripts.enhance import main as enhance_main
    from scripts.ocr import main as ocr_main
    from scripts.review import main as review_main
    from scripts.corpus import main as corpus_main

    print("=" * 60)
    print("🚀 FULL PIPELINE")
    print("=" * 60)

    # Stage 1: Extract
    print("\n" + "─" * 60)
    print("📄 Stage 1/5: EXTRACT")
    print("─" * 60)
    extract_argv = list(args.targets) if args.targets else []
    if args.dpi:
        extract_argv.extend(["--dpi", str(args.dpi)])
    books = extract_main(extract_argv)

    # Stage 2: Enhance
    print("\n" + "─" * 60)
    print("✨ Stage 2/5: ENHANCE")
    print("─" * 60)
    enhance_argv = ["--targets"] + books if books else []
    if args.docres:
        enhance_argv.append("--docres")
    if args.docres_tasks:
        enhance_argv.extend(["--docres-tasks"] + list(args.docres_tasks))
    if args.prepocr:
        enhance_argv.append("--prepocr")
    if args.classical:
        enhance_argv.append("--classical")
    enhance_main(enhance_argv)

    # Stage 3: OCR
    print("\n" + "─" * 60)
    print("🔍 Stage 3/5: OCR")
    print("─" * 60)
    ocr_argv = ["--targets"] + books if books else []
    if args.model:
        ocr_argv.extend(["--model", args.model])
    if args.debug:
        ocr_argv.append("--debug")
    if args.limit:
        ocr_argv.extend(["--limit", str(args.limit)])
    ocr_main(ocr_argv)

    # Stage 4: Review
    print("\n" + "─" * 60)
    print("🧹 Stage 4/5: REVIEW")
    print("─" * 60)
    review_argv = books if books else []
    if args.model:
        review_argv.extend(["--model", args.model])
    review_argv.append("--yes")  # Non-interactive in pipeline mode
    review_main(review_argv)

    # Stage 5: Corpus
    print("\n" + "─" * 60)
    print("📚 Stage 5/5: CORPUS")
    print("─" * 60)
    corpus_argv = ["--targets"] + books if books else []
    corpus_main(corpus_argv)

    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE")
    if books:
        print(f"   Books processed: {', '.join(books)}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="OCR Pipeline — Breton-French corpus extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s run                            Full pipeline, all PDFs
  %(prog)s run pdfs/my_book.pdf           Full pipeline, one PDF
  %(prog)s extract                        Extract pages from all PDFs
  %(prog)s enhance --docres --prepocr      Enhance with AI restoration
  %(prog)s ocr Manuel_1865                OCR one specific book
  %(prog)s evaluate                       Compute CER & WER on all reference books
""",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- run ---
    p_run = subparsers.add_parser("run", help="Run full pipeline end-to-end")
    p_run.add_argument(
        "targets", nargs="*", help="PDF file(s) to process (default: all)"
    )
    p_run.add_argument("--dpi", type=int, help="DPI for extraction (default: 300)")
    p_run.add_argument(
        "--docres",
        action="store_true",
        default=False,
        help="Enable DocRes AI enhancement (requires --with-enhance setup)",
    )
    p_run.add_argument(
        "--docres-tasks",
        nargs="+",
        choices=["deshadowing", "deblurring", "appearance"],
        default=None,
        help="DocRes tasks to run, in order (default: deshadowing deblurring appearance)",
    )
    p_run.add_argument(
        "--prepocr",
        action="store_true",
        default=False,
        help="Enable PreP-OCR ResShift diffusion deblurring (requires --with-enhance setup)",
    )
    p_run.add_argument(
        "--classical",
        dest="classical",
        action="store_true",
        default=False,
        help="Enable classical enhancement (grayscale + CLAHE)",
    )
    p_run.add_argument(
        "--model",
        default=None,
        help="OpenAI model to use for OCR (default: from ocr.py)",
    )
    p_run.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Debug mode: print full prompts and LLM responses during OCR.",
    )
    p_run.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only N random pages per book for OCR (for testing).",
    )
    p_run.set_defaults(func=cmd_run)

    # --- extract ---
    p_extract = subparsers.add_parser("extract", help="Extract PDF pages as PNGs")
    p_extract.add_argument(
        "targets", nargs="*", help="PDF file(s) to process (default: all)"
    )
    p_extract.add_argument("--dpi", type=int, help="DPI for extraction (default: 300)")
    p_extract.set_defaults(func=cmd_extract)

    # --- enhance ---
    p_enhance = subparsers.add_parser("enhance", help="Enhance page images")
    p_enhance.add_argument(
        "targets",
        nargs="*",
        help="Book folder(s) or image file(s) to process (default: all)",
    )
    p_enhance.add_argument(
        "--docres",
        action="store_true",
        default=False,
        help="Enable DocRes AI enhancement (requires --with-enhance setup)",
    )
    p_enhance.add_argument(
        "--docres-tasks",
        nargs="+",
        choices=["deshadowing", "deblurring", "appearance"],
        default=None,
        help="DocRes tasks to run, in order (default: deshadowing deblurring appearance)",
    )
    p_enhance.add_argument(
        "--prepocr",
        action="store_true",
        default=False,
        help="Enable PreP-OCR ResShift diffusion deblurring (requires --with-enhance setup)",
    )
    p_enhance.add_argument(
        "--classical",
        dest="classical",
        action="store_true",
        default=False,
        help="Enable classical enhancement (grayscale + CLAHE)",
    )
    p_enhance.set_defaults(func=cmd_enhance)

    # --- compare ---
    p_compare = subparsers.add_parser(
        "compare",
        help="Generate comparison matrix of all enhancement permutations",
    )
    p_compare.add_argument(
        "image",
        help="Path to a single input image (e.g. pages/my_book/17.png)",
    )
    p_compare.set_defaults(func=cmd_compare)

    # --- ignore ---
    p_ignore = subparsers.add_parser(
        "ignore",
        help="Add page(s) to the per-book droplist",
    )
    p_ignore.add_argument(
        "images",
        nargs="+",
        help="Image file(s) to ignore (e.g. pages_enhanced/my_book/05.png)",
    )
    p_ignore.set_defaults(func=cmd_ignore)

    # --- ocr ---
    p_ocr = subparsers.add_parser("ocr", help="Run OCR extraction via OpenAI VLM")
    p_ocr.add_argument(
        "targets", nargs="*", help="Book folder(s) to process (default: all)"
    )
    p_ocr.add_argument(
        "--model",
        default=None,
        help="Model to use (default: from ocr.py). Supports OpenAI and Claude models.",
    )
    p_ocr.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output directory for JSONL files (default: ocr/<book>/<model>/)",
    )
    p_ocr.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Debug mode: print full prompts and LLM responses.",
    )
    p_ocr.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only N random pages per book (for testing).",
    )
    p_ocr.set_defaults(func=cmd_ocr)

    # --- review ---
    p_review = subparsers.add_parser(
        "review", help="Copy OCR output to review/ and run quality assurance"
    )
    p_review.add_argument(
        "targets",
        nargs="*",
        help="Book folder(s) to review. Default: all books in ocr/.",
    )
    p_review.add_argument(
        "--model",
        default=None,
        help="Model subfolder to copy from (default: antigravity).",
    )
    p_review.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Skip confirmation prompts (non-interactive mode).",
    )
    p_review.set_defaults(func=cmd_review)

    # --- evaluate ---
    p_evaluate = subparsers.add_parser(
        "evaluate", help="Compute WER and CER for OCR outputs against human reference"
    )
    p_evaluate.add_argument(
        "targets", nargs="*", help="Book folder(s) to evaluate (default: all in error_rates/)"
    )
    p_evaluate.set_defaults(func=cmd_evaluate)

    # --- corpus ---
    p_corpus = subparsers.add_parser("corpus", help="Build corpus from reviewed output")
    p_corpus.add_argument(
        "targets", nargs="*", help="Book folder(s) to process (default: all in review/)"
    )
    p_corpus.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output root directory (default: corpus/).",
    )
    p_corpus.set_defaults(func=cmd_corpus)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
