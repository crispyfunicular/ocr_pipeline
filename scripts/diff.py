#!/usr/bin/env python3
"""
JSONL diff — compare two directories (or files) of JSONL data.

Matches .jsonl files by filename within each directory and reports
added, removed, and modified entries line-by-line.
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_A = PROJECT_ROOT / "ocr"
DEFAULT_B = PROJECT_ROOT / "review"

# ANSI colours
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"


def load_jsonl(path: Path) -> list[str]:
    """Read a JSONL file and return non-empty stripped lines."""
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []
    return [line.strip() for line in content.splitlines() if line.strip()]


def format_entry(line: str) -> str:
    """Pretty-format a JSONL line for display."""
    try:
        data = json.loads(line)
        br = data.get("breton", "")
        fr = data.get("français", "")
        return f"{br}  →  {fr}"
    except json.JSONDecodeError:
        return line


def diff_files(path_a: Path, path_b: Path, verbose: bool = False) -> tuple[int, int, int]:
    """Diff two JSONL files line-by-line.

    Returns (added, removed, modified) counts.
    """
    lines_a = load_jsonl(path_a)
    lines_b = load_jsonl(path_b)

    added = 0
    removed = 0
    modified = 0

    max_len = max(len(lines_a), len(lines_b))

    for i in range(max_len):
        if i >= len(lines_a):
            added += 1
            if verbose:
                print(f"  {GREEN}+ {format_entry(lines_b[i])}{RESET}")
        elif i >= len(lines_b):
            removed += 1
            if verbose:
                print(f"  {RED}- {format_entry(lines_a[i])}{RESET}")
        elif lines_a[i] != lines_b[i]:
            modified += 1
            if verbose:
                print(f"  {RED}- {format_entry(lines_a[i])}{RESET}")
                print(f"  {GREEN}+ {format_entry(lines_b[i])}{RESET}")

    return added, removed, modified


def diff_dirs(dir_a: Path, dir_b: Path, verbose: bool = False) -> None:
    """Diff all matching .jsonl files in two directories."""
    files_a = {f.name: f for f in sorted(dir_a.glob("*.jsonl"))}
    files_b = {f.name: f for f in sorted(dir_b.glob("*.jsonl"))}

    all_names = sorted(set(files_a) | set(files_b))

    if not all_names:
        print("ℹ️  No .jsonl files found in either directory.")
        return

    grand_added = 0
    grand_removed = 0
    grand_modified = 0

    for name in all_names:
        if name not in files_a:
            count = len(load_jsonl(files_b[name]))
            print(f"  {GREEN}{name}: new file ({count} entries){RESET}")
            grand_added += count
            continue

        if name not in files_b:
            count = len(load_jsonl(files_a[name]))
            print(f"  {RED}{name}: removed ({count} entries){RESET}")
            grand_removed += count
            continue

        if verbose:
            print(f"  {CYAN}{name}:{RESET}")

        added, removed, modified = diff_files(files_a[name], files_b[name], verbose)
        total = added + removed + modified

        if total == 0:
            continue

        parts = []
        if added:
            parts.append(f"{GREEN}+{added}{RESET}")
        if removed:
            parts.append(f"{RED}-{removed}{RESET}")
        if modified:
            parts.append(f"{YELLOW}~{modified}{RESET}")

        label = f"  {name}: " + ", ".join(parts)
        if not verbose:
            print(label)

        grand_added += added
        grand_removed += removed
        grand_modified += modified

    # Grand totals
    grand_total = grand_added + grand_removed + grand_modified
    print()
    if grand_total == 0:
        print(f"✅ No differences found ({len(all_names)} files compared).")
    else:
        parts = []
        if grand_added:
            parts.append(f"{GREEN}+{grand_added} added{RESET}")
        if grand_removed:
            parts.append(f"{RED}-{grand_removed} removed{RESET}")
        if grand_modified:
            parts.append(f"{YELLOW}~{grand_modified} modified{RESET}")
        print(f"📊 {', '.join(parts)}  ({len(all_names)} files compared)")


def main(argv=None):
    """Entry point. Pass argv list for programmatic use, or None for CLI."""
    parser = argparse.ArgumentParser(
        description="Compare two JSONL directories or files and report differences.",
    )
    parser.add_argument(
        "source_a",
        nargs="?",
        default=str(DEFAULT_A),
        help="Left side: directory or .jsonl file (default: ocr/).",
    )
    parser.add_argument(
        "source_b",
        nargs="?",
        default=str(DEFAULT_B),
        help="Right side: directory or .jsonl file (default: review/).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show individual changed lines.",
    )
    args = parser.parse_args(argv)

    path_a = Path(args.source_a)
    path_b = Path(args.source_b)

    if not path_a.exists():
        print(f"❌ Not found: {path_a}", file=sys.stderr)
        sys.exit(1)
    if not path_b.exists():
        print(f"❌ Not found: {path_b}", file=sys.stderr)
        sys.exit(1)

    # Both files
    if path_a.is_file() and path_b.is_file():
        print(f"📄 {path_a.name}  ↔  {path_b.name}")
        added, removed, modified = diff_files(path_a, path_b, verbose=args.verbose)
        total = added + removed + modified
        if total == 0:
            print("✅ No differences.")
        else:
            parts = []
            if added:
                parts.append(f"{GREEN}+{added} added{RESET}")
            if removed:
                parts.append(f"{RED}-{removed} removed{RESET}")
            if modified:
                parts.append(f"{YELLOW}~{modified} modified{RESET}")
            print(f"📊 {', '.join(parts)}")
        return

    # Both directories
    if path_a.is_dir() and path_b.is_dir():
        print(f"📂 {path_a}  ↔  {path_b}")
        print()
        diff_dirs(path_a, path_b, verbose=args.verbose)
        return

    # Mismatch
    print(
        "❌ Both sources must be the same type (both files or both directories).",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
