"""
OCR pipeline step — bilingual Breton-French corpus extraction.

Sends page images to a VLM (OpenAI, Anthropic Claude, or Google Gemini),
parses structured JSONL output + quality report.

Usage:
    python -m src.ocr [targets ...] [--model X] [--batch] [--debug]
    python pipeline.py ocr [targets ...] [--model X] [--batch] [--debug]
"""

from pathlib import Path

from src.ocr.core import DEFAULT_MODEL, parse_vlm_response  # noqa: F401

__all__ = ["main", "DEFAULT_MODEL", "parse_vlm_response"]


def main(argv=None):
    """Unified OCR entry point.  Pass argv list for programmatic use, or None for CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="OCR extraction of bilingual Breton-French corpus using VLM.",
    )
    parser.add_argument(
        "targets",
        nargs="*",
        default=None,
        help="Book subdirectory name(s) under pages/ or individual image file path(s). Default: all.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"VLM model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output path (bypasses run-folder structure). "
        "For a single image: directory or .jsonl file path.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Debug mode: print full prompts and LLM responses.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only N random pages per book (for testing).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible --limit sampling.",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        default=False,
        help="Use Gemini Batch API (async, 50%% cost).  Gemini models only.",
    )
    parser.add_argument(
        "--main-prompt",
        type=Path,
        default=None,
        help="Override the main system prompt file (default: prompts/extract_bilingual_corpus.md).",
    )
    parser.add_argument(
        "--book-prompt",
        type=Path,
        default=None,
        help="Override the book-specific prompt file (default: auto-detected from book name).",
    )
    args = parser.parse_args(argv)

    if args.batch:
        from src.ocr.batch import run_batch

        run_batch(args)
    else:
        from src.ocr.sync import run_sync

        run_sync(args)


if __name__ == "__main__":
    main()
