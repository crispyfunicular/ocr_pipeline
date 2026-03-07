#!/usr/bin/env python3
"""
Build corpus — read per-page JSONL from ocr/<book>/<model>/, deduplicate,
and write one corpus/<book>.jsonl per book.

Selects a single model's output per book (default: antigravity), removes
exact duplicate {breton, français} pairs, and writes the merged result.
"""

import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OCR_DIR = PROJECT_ROOT / "ocr"
DEFAULT_CORPUS_DIR = PROJECT_ROOT / "corpus"
DEFAULT_MODEL = "antigravity"


def build_book_corpus(
    book_name: str,
    model: str,
    corpus_root: Path,
) -> tuple[int, int, int]:
    """Read, deduplicate, and merge JSONL for one book.

    Returns (total_raw, duplicates_removed, final_count).
    """
    src_dir = OCR_DIR / book_name / model
    if not src_dir.exists():
        print(f"  ⚠️  Model folder not found: {src_dir.relative_to(PROJECT_ROOT)}")
        return 0, 0, 0

    jsonl_files = sorted(src_dir.glob("*.jsonl"))
    if not jsonl_files:
        print(f"  ⚠️  No JSONL files in {src_dir.relative_to(PROJECT_ROOT)}")
        return 0, 0, 0

    seen: set[tuple[str, str]] = set()
    unique_lines: list[str] = []
    total_raw = 0

    for f in jsonl_files:
        content = f.read_text(encoding="utf-8").strip()
        if not content:
            continue  # Skip empty files (OCR error placeholders)

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            total_raw += 1
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # Keep malformed lines as-is (they'll be flagged by review)
                unique_lines.append(line)
                continue

            key = (data.get("breton", ""), data.get("français", ""))
            if key not in seen:
                seen.add(key)
                unique_lines.append(line)

    duplicates = total_raw - len(unique_lines)

    # Write merged file
    corpus_root.mkdir(parents=True, exist_ok=True)
    out_path = corpus_root / f"{book_name}.jsonl"
    out_path.write_text("\n".join(unique_lines) + "\n", encoding="utf-8")

    return total_raw, duplicates, len(unique_lines)


def main(argv=None):
    """Entry point. Pass argv list for programmatic use, or None for CLI."""
    parser = argparse.ArgumentParser(
        description="Build corpus: deduplicate and merge per-page JSONL from ocr/<book>/<model>/ into corpus/<book>.jsonl.",
    )
    parser.add_argument(
        "--targets",
        nargs="*",
        help="Book folder(s) to process. Default: all books in ocr/.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model subfolder to use as source (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output root directory (default: corpus/).",
    )
    args = parser.parse_args(argv)

    corpus_root = args.output if args.output is not None else DEFAULT_CORPUS_DIR

    # Discover books
    if args.targets:
        books = args.targets
    else:
        if not OCR_DIR.exists():
            print(f"❌ OCR directory not found: {OCR_DIR}")
            return
        books = sorted(
            d.name for d in OCR_DIR.iterdir()
            if d.is_dir() and (d / args.model).is_dir()
        )

    if not books:
        print("ℹ️  No books found to process.")
        return

    print(f"📚 Building corpus from {len(books)} book(s) (model: {args.model})")
    print(f"📂 Output: {corpus_root.resolve()}/")

    grand_raw = 0
    grand_dupes = 0
    grand_final = 0

    for book in books:
        print(f"\n  📖 {book}")
        total_raw, duplicates, final_count = build_book_corpus(
            book, args.model, corpus_root
        )
        grand_raw += total_raw
        grand_dupes += duplicates
        grand_final += final_count

        dupe_info = f" (−{duplicates} duplicates)" if duplicates else ""
        print(f"     {total_raw} → {final_count} pairs{dupe_info} → corpus/{book}.jsonl")

    print(f"\n{'═' * 60}")
    print(f"✅ Corpus built: {grand_raw} → {grand_final} pairs (−{grand_dupes} duplicates)")
    print(f"   Output: {corpus_root.resolve()}/")
    print(f"{'═' * 60}")


if __name__ == "__main__":
    main()
