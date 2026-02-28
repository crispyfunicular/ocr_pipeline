#!/usr/bin/env python3
"""
Build final corpus — merge per-page JSONL into unified corpus files.

🚧 Stub — not yet implemented.
"""

import argparse
from pathlib import Path


def main(argv=None):
    """Entry point. Pass argv list for programmatic use, or None for CLI."""
    parser = argparse.ArgumentParser(
        description="Merge per-page JSONL into final bilingual corpus (stub).",
    )
    parser.add_argument(
        "--targets",
        nargs="*",
        help="Book folder(s) to process. Default: all.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output directory or file for final corpus (stub, not yet used).",
    )
    args = parser.parse_args(argv)

    print("🚧 Corpus build step not yet implemented.")
    if args.targets:
        print(f"   Would process: {', '.join(args.targets)}")


if __name__ == "__main__":
    main()
