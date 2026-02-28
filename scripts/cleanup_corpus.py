#!/usr/bin/env python3
"""
Corpus cleanup — quality assurance on extracted JSONL.

🚧 Stub — not yet implemented.
"""

import argparse
from pathlib import Path


def main(argv=None):
    """Entry point. Pass argv list for programmatic use, or None for CLI."""
    parser = argparse.ArgumentParser(
        description="Quality assurance on extracted JSONL corpus (stub).",
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
        help="Output directory for cleaned JSONL (stub, not yet used).",
    )
    args = parser.parse_args(argv)

    print("🚧 Cleanup step not yet implemented.")
    if args.targets:
        print(f"   Would process: {', '.join(args.targets)}")


if __name__ == "__main__":
    main()
