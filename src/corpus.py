#!/usr/bin/env python3
"""
Build corpus — read per-page JSONL from an OCR extraction run's extracted/
directory, deduplicate {breton, français} pairs, and write
<run>/corpus/<book>.jsonl.

Usage:
    python -m src.corpus ocr/bozec_methode_1933/gemini-3.1-pro-preview/0002-20260314-1759
    python -m src.corpus                      # auto-discover all completed runs
    python pipeline.py corpus                 # same, via the pipeline CLI
"""

import argparse
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OCR_ROOT = PROJECT_ROOT / "ocr"

STATE_FILENAME = "run_state.json"
EXTRACTED_DIR = "extracted"
CORPUS_DIR = "corpus"

# Matches run folder names: NNNN-YYYYMMDD-HHMM
RUN_FOLDER_RE = re.compile(r"^\d{4}-\d{8}-\d{4}$")


def _load_run_state(run_dir: Path) -> dict | None:
    """Load run_state.json from a run directory."""
    p = run_dir / STATE_FILENAME
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _corpus_path(run_dir: Path, book_name: str) -> Path:
    """Return the path to the corpus JSONL inside a run folder."""
    return run_dir / CORPUS_DIR / f"{book_name}.jsonl"


def build_run_corpus(
    run_dir: Path,
    book_name: str,
    output_dir: Path | None = None,
) -> tuple[int, int, int]:
    """Read, deduplicate, and merge JSONL for one run.

    Args:
        run_dir: Path to the run folder (e.g. ocr/<book>/<model>/<run>/).
        book_name: Book name for the output filename.
        output_dir: Optional override — write to <output_dir>/<book>.jsonl
                    instead of <run>/corpus/<book>.jsonl.

    Returns:
        (total_raw, duplicates_removed, final_count).
    """
    src_dir = run_dir / EXTRACTED_DIR
    if not src_dir.exists():
        print(f"  ⚠️  Extracted folder not found: {src_dir}")
        return 0, 0, 0

    jsonl_files = sorted(src_dir.glob("*.jsonl"))
    if not jsonl_files:
        print(f"  ⚠️  No JSONL files in {src_dir}")
        return 0, 0, 0

    seen: set[tuple[str, str]] = set()
    unique_lines: list[str] = []
    total_raw = 0

    for f in jsonl_files:
        content = f.read_text(encoding="utf-8").strip()
        if not content:
            continue

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            total_raw += 1
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # Keep malformed lines as-is (they'll be flagged later)
                unique_lines.append(line)
                continue

            key = (data.get("breton", ""), data.get("français", ""))
            if key not in seen:
                seen.add(key)
                unique_lines.append(line)

    duplicates = total_raw - len(unique_lines)

    # Sort alphabetically by 'breton' field; malformed lines sink to the end
    def sort_key(raw_line: str) -> str:
        try:
            return json.loads(raw_line).get("breton", "").casefold()
        except json.JSONDecodeError:
            return "\xff" + raw_line

    unique_lines.sort(key=sort_key)

    # Write merged file
    if output_dir is not None:
        out_root = output_dir
    else:
        out_root = run_dir / CORPUS_DIR

    out_root.mkdir(parents=True, exist_ok=True)
    out_path = out_root / f"{book_name}.jsonl"
    out_path.write_text("\n".join(unique_lines) + "\n", encoding="utf-8")

    return total_raw, duplicates, len(unique_lines)


def discover_completed_runs(ocr_root: Path) -> list[tuple[Path, str]]:
    """Find all completed runs that don't yet have a corpus/<book>.jsonl.

    Scans ocr/<book>/<model>/<run>/ for run_state.json with status "completed"
    and no existing corpus JSONL.

    Returns:
        List of (run_dir, book_name) tuples.
    """
    results: list[tuple[Path, str]] = []

    if not ocr_root.exists():
        return results

    for book_dir in sorted(ocr_root.iterdir()):
        if not book_dir.is_dir():
            continue
        book_name = book_dir.name

        for model_dir in sorted(book_dir.iterdir()):
            if not model_dir.is_dir():
                continue

            for run_dir in sorted(model_dir.iterdir()):
                if not run_dir.is_dir() or not RUN_FOLDER_RE.match(run_dir.name):
                    continue

                state = _load_run_state(run_dir)
                if not state or state.get("status") != "completed":
                    continue

                if _corpus_path(run_dir, book_name).exists():
                    continue

                results.append((run_dir, book_name))

    return results


def _resolve_run_dir(target: str) -> tuple[Path, str]:
    """Resolve a target string to (run_dir, book_name).

    Accepts:
      - A path to a run folder (absolute or relative)

    Raises SystemExit on invalid target.
    """
    run_dir = Path(target).resolve()

    if not run_dir.is_dir():
        print(f"❌ Not a directory: {target}")
        raise SystemExit(1)

    # Validate it looks like a run folder
    state = _load_run_state(run_dir)
    if state and "book" in state:
        return run_dir, state["book"]

    # Try to infer book name from path: ocr/<book>/<model>/<run>/
    parts = run_dir.parts
    if len(parts) >= 4:
        book_name = parts[-3]  # ocr/<book>/<model>/<run>
        return run_dir, book_name

    print(f"❌ Cannot determine book name for: {target}")
    print("   Expected: ocr/<book>/<model>/<run>/ or a folder with run_state.json")
    raise SystemExit(1)


def main(argv=None):
    """Entry point. Pass argv list for programmatic use, or None for CLI."""
    parser = argparse.ArgumentParser(
        description=(
            "Build corpus: deduplicate and merge per-page JSONL from "
            "an OCR extraction run's extracted/ directory."
        ),
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help=(
            "Run folder path(s) to process "
            "(e.g. ocr/bozec.../gemini.../0002-...). "
            "Default: all completed runs missing a corpus JSONL."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Override output directory (default: <run>/corpus/).",
    )
    args = parser.parse_args(argv)

    output_dir = args.output

    # Discover targets
    if args.targets:
        runs = [_resolve_run_dir(t) for t in args.targets]
    else:
        runs = discover_completed_runs(OCR_ROOT)

    if not runs:
        print("ℹ️  No runs to process (all completed runs already have corpus JSONL).")
        return

    print(f"📚 Building corpus from {len(runs)} run(s)")

    grand_raw = 0
    grand_dupes = 0
    grand_final = 0

    for run_dir, book_name in runs:
        # Show a human-readable relative path
        try:
            rel = run_dir.relative_to(PROJECT_ROOT)
        except ValueError:
            rel = run_dir
        print(f"\n  📖 {book_name}  ({rel})")

        total_raw, duplicates, final_count = build_run_corpus(
            run_dir, book_name, output_dir
        )
        grand_raw += total_raw
        grand_dupes += duplicates
        grand_final += final_count

        if total_raw > 0:
            dupe_info = f" (−{duplicates} duplicates)" if duplicates else ""
            out_label = (
                f"{output_dir}/{book_name}.jsonl"
                if output_dir
                else f"corpus/{book_name}.jsonl"
            )
            print(f"     {total_raw} → {final_count} pairs{dupe_info} → {out_label}")

    print(f"\n{'═' * 60}")
    print(
        f"✅ Corpus built: {grand_raw} → {grand_final} pairs (−{grand_dupes} duplicates)"
    )
    print(f"{'═' * 60}")


if __name__ == "__main__":
    main()
