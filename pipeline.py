#!/usr/bin/env python3
"""
Unified OCR pipeline CLI for Breton-French corpus extraction.

Stages:
    extract   — PDF → PNG pages (300 DPI)
    enhance   — Image enhancement (CLAHE + optional DocRes AI)
    ocr       — VLM-based bilingual text extraction (OpenAI / Anthropic)
    cleanup   — JSONL quality assurance (stub)
    corpus    — Merge JSONL into final corpus (stub)
    run       — Chain all stages end-to-end

Usage:
    python pipeline.py run                          # full pipeline, all PDFs
    python pipeline.py run pdfs/my_book.pdf         # full pipeline, one PDF
    python pipeline.py extract                      # extract only, all PDFs
    python pipeline.py enhance --no-docres             # enhance without AI
    python pipeline.py ocr Manuel_1865             # OCR one book
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def cmd_extract(args):
    """Extract pages from PDFs."""
    from scripts.extract_pages import main as extract_main

    argv = list(args.targets) if args.targets else []
    if args.dpi:
        argv.extend(["--dpi", str(args.dpi)])
    return extract_main(argv)


def cmd_enhance(args):
    """Enhance extracted pages."""
    from scripts.enhance_pages import main as enhance_main

    argv = []
    if args.targets:
        argv.extend(["--targets"] + list(args.targets))
    if not args.docres:
        argv.append("--no-docres")
    if args.docres_tasks:
        argv.extend(["--docres-tasks"] + list(args.docres_tasks))
    return enhance_main(argv)


def cmd_ocr(args):
    """Run OCR extraction."""
    from scripts.ocr_openai import main as ocr_main

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


def cmd_cleanup(args):
    """Run corpus cleanup (stub)."""
    from scripts.cleanup_corpus import main as cleanup_main

    argv = []
    if args.targets:
        argv.extend(["--targets"] + list(args.targets))
    if args.output:
        argv.extend(["--output", str(args.output)])
    return cleanup_main(argv)


def cmd_corpus(args):
    """Build final corpus (stub)."""
    from scripts.build_corpus import main as corpus_main

    argv = []
    if args.targets:
        argv.extend(["--targets"] + list(args.targets))
    if args.output:
        argv.extend(["--output", str(args.output)])
    return corpus_main(argv)


def cmd_run(args):
    """Run the full pipeline end-to-end."""
    from scripts.extract_pages import main as extract_main
    from scripts.enhance_pages import main as enhance_main
    from scripts.ocr_openai import main as ocr_main
    from scripts.cleanup_corpus import main as cleanup_main
    from scripts.build_corpus import main as corpus_main

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
    if not args.docres:
        enhance_argv.append("--no-docres")
    if args.docres_tasks:
        enhance_argv.extend(["--docres-tasks"] + list(args.docres_tasks))
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

    # Stage 4: Cleanup
    print("\n" + "─" * 60)
    print("🧹 Stage 4/5: CLEANUP")
    print("─" * 60)
    cleanup_argv = ["--targets"] + books if books else []
    cleanup_main(cleanup_argv)

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
  %(prog)s enhance --no-docres               Enhance without AI restoration
  %(prog)s ocr Manuel_1865                OCR one specific book
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
        "--no-docres",
        dest="docres",
        action="store_false",
        default=True,
        help="Disable DocRes AI enhancement (on by default)",
    )
    p_run.add_argument(
        "--docres-tasks",
        nargs="+",
        choices=["deshadowing", "deblurring", "appearance"],
        default=None,
        help="DocRes tasks to run, in order (default: deshadowing deblurring appearance)",
    )
    p_run.add_argument(
        "--model",
        default=None,
        help="OpenAI model to use for OCR (default: from ocr_openai.py)",
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
        "--no-docres",
        dest="docres",
        action="store_false",
        default=True,
        help="Disable DocRes AI enhancement (on by default)",
    )
    p_enhance.add_argument(
        "--docres-tasks",
        nargs="+",
        choices=["deshadowing", "deblurring", "appearance"],
        default=None,
        help="DocRes tasks to run, in order (default: deshadowing deblurring appearance)",
    )
    p_enhance.set_defaults(func=cmd_enhance)

    # --- ocr ---
    p_ocr = subparsers.add_parser("ocr", help="Run OCR extraction via OpenAI VLM")
    p_ocr.add_argument(
        "targets", nargs="*", help="Book folder(s) to process (default: all)"
    )
    p_ocr.add_argument(
        "--model",
        default=None,
        help="Model to use (default: from ocr_openai.py). Supports OpenAI and Claude models.",
    )
    p_ocr.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output directory for JSONL files (default: corpus/<book>/<model>/)",
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

    # --- cleanup ---
    p_cleanup = subparsers.add_parser(
        "cleanup", help="Quality assurance on extracted JSONL"
    )
    p_cleanup.add_argument(
        "targets", nargs="*", help="Book folder(s) to process (default: all)"
    )
    p_cleanup.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output directory for cleaned JSONL (stub).",
    )
    p_cleanup.set_defaults(func=cmd_cleanup)

    # --- corpus ---
    p_corpus = subparsers.add_parser("corpus", help="Build final merged corpus")
    p_corpus.add_argument(
        "targets", nargs="*", help="Book folder(s) to process (default: all)"
    )
    p_corpus.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output directory or file for final corpus (stub).",
    )
    p_corpus.set_defaults(func=cmd_corpus)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
