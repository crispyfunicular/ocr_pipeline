#!/usr/bin/env python3
"""
Corpus review — quality assurance on extracted JSONL.

Scans JSONL files for common errors (missing keys, invalid characters, length imbalances)
and generates a Markdown report of flagged entries.
"""

import argparse
import collections
import json
import re
import sys
from pathlib import Path

# Required keys
REQUIRED_KEYS = {"breton", "français"}

# Approved character sets (upper and lower case included where relevant)
BRETON_CHARS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "ÀÂÄÉÈÊËÏÎÔÙÛÜŸÑÇàâäéèêëïîôùûüÿñç' .,;:!?…—–-()\"«»"
)
FRENCH_CHARS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "ÀÂÄÆÉÈÊËÏÎÔŒÙÛÜŸÇàâäæéèêëïîôœùûüÿç' .,;:!?…—–-()\"«»"
)

# Common variables
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OCR_DIR = PROJECT_ROOT / "ocr"
REPORTS_DIR = PROJECT_ROOT / "reports"

CheckResult = collections.namedtuple(
    "CheckResult", ["level", "rule", "message", "breton", "francais"]
)


def check_entry(data: dict, seen_pairs: set) -> list[CheckResult]:
    """Run all checks on a single parsed JSON object."""
    results = []

    br = data.get("breton", "")
    fr = data.get("français", "")

    # 2. Missing keys
    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        results.append(
            CheckResult(
                "🔴 ERROR", "Missing keys", f"Missing {', '.join(missing)}", br, fr
            )
        )
        return results  # Stop here if we don't have the keys

    # 10. Unexpected extra keys
    extra = set(data.keys()) - REQUIRED_KEYS
    if extra:
        results.append(
            CheckResult(
                "🟡 WARNING", "Extra keys", f"Unexpected {', '.join(extra)}", br, fr
            )
        )

    # Handle non-string types gracefully
    if not isinstance(br, str) or not isinstance(fr, str):
        results.append(
            CheckResult(
                "🔴 ERROR",
                "Type error",
                "Values must be strings",
                str(type(br)),
                str(type(fr)),
            )
        )
        return results

    # 3. Empty value
    if not br.strip():
        results.append(
            CheckResult("🔴 ERROR", "Empty value", "Breton is empty", br, fr)
        )
    if not fr.strip():
        results.append(
            CheckResult("🔴 ERROR", "Empty value", "French is empty", br, fr)
        )

    if not br.strip() or not fr.strip():
        return results  # Stop further text checks

    # 11. Leading/trailing whitespace
    if br != br.strip() or fr != fr.strip():
        results.append(
            CheckResult(
                "🟡 WARNING",
                "Whitespace",
                "Leading or trailing whitespace detected",
                f"'{br}'",
                f"'{fr}'",
            )
        )

    # 4 & 5. Invalid characters
    br_invalid = set(br) - BRETON_CHARS
    if br_invalid:
        results.append(
            CheckResult(
                "🟡 WARNING",
                "Invalid chars (BR)",
                f"Invalid chars: {''.join(br_invalid)}",
                br,
                fr,
            )
        )

    fr_invalid = set(fr) - FRENCH_CHARS
    if fr_invalid:
        results.append(
            CheckResult(
                "🟡 WARNING",
                "Invalid chars (FR)",
                f"Invalid chars: {''.join(fr_invalid)}",
                br,
                fr,
            )
        )

    # 6. Length ratio imbalance
    len_br = len(br)
    len_fr = len(fr)
    if len_br > 0 and len_fr > 0:
        ratio = max(len_br / len_fr, len_fr / len_br)
        if ratio >= 3.0 and max(len_br, len_fr) >= 32:
            results.append(
                CheckResult(
                    "🟡 WARNING",
                    "Length imbalance",
                    f"Ratio {ratio:.1f}x (br: {len_br}, fr: {len_fr})",
                    br,
                    fr,
                )
            )

    # 7. Duplicate pair
    # (Disabled: we will deduplicate later)
    # pair_tuple = (br.strip(), fr.strip())
    # if pair_tuple in seen_pairs:
    #     results.append(
    #         CheckResult(
    #             "🟡 WARNING",
    #             "Duplicate",
    #             "Exact pair already seen",
    #             f"br: {br} | fr: {fr}",
    #         )
    #     )
    # seen_pairs.add(pair_tuple)

    # 8. Suspicious single-char entry
    if len_br == 1 or len_fr == 1:
        results.append(
            CheckResult(
                "🟡 WARNING",
                "Single char",
                "One side is a single character",
                br,
                fr,
            )
        )

    # 8b. Extremely long entry
    if len_br > 256 or len_fr > 256:
        results.append(
            CheckResult(
                "🟡 WARNING",
                "Extremely long",
                "One side is strictly longer than 256 characters",
                br,
                fr,
            )
        )

    # 9. Digit-only entry
    def is_mostly_digits(s):
        return bool(re.match(r"^[\d\s.,;:!?…—–\-()\"«»]+$", s))

    if is_mostly_digits(br) or is_mostly_digits(fr):
        results.append(
            CheckResult(
                "🟡 WARNING",
                "Digit only",
                "Entry contains no letters",
                br,
                fr,
            )
        )

    # 12. Truncated entries
    if (
        br.endswith("...")
        or br.endswith("–")
        or fr.endswith("...")
        or fr.endswith("–")
        or br.endswith("-")
        or fr.endswith("-")
    ):
        results.append(
            CheckResult(
                "🟡 WARNING",
                "Truncated",
                "Value ends with truncation marker",
                br,
                fr,
            )
        )

    # 13. Identical breton/français
    if br.strip() == fr.strip():
        results.append(
            CheckResult(
                "🟡 WARNING",
                "Identical",
                "Breton and French are exactly identical",
                br,
                fr,
            )
        )

    return results


def review_file(
    jsonl_path: Path, seen_pairs: set
) -> list[tuple[int, list[CheckResult]]]:
    """Review a single JSONL file and return a list of (line_num, results)."""
    file_issues = []
    try:
        lines = jsonl_path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        return [
            (
                0,
                [
                    CheckResult(
                        "🔴 ERROR", "File read", f"Failed to read file: {e}", "", ""
                    )
                ],
            )
        ]

    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            file_issues.append(
                (i, [CheckResult("🔴 ERROR", "JSON parse error", str(e), line, "")])
            )
            continue

        # Check parsed object
        results = check_entry(data, seen_pairs)
        if results:
            file_issues.append((i, results))

    return file_issues


def review_target(target_dir: Path, out_report: Path):
    """Review all JSONL files in a directory and generate a report."""
    print(f"🔍 Reviewing {target_dir}")

    if target_dir.is_file():
        jsonl_files = [target_dir]
    else:
        jsonl_files = sorted(list(target_dir.rglob("*.jsonl")))

    if not jsonl_files:
        print(f"  ⚠️ No JSONL files found in {target_dir}")
        return

    seen_pairs = set()
    all_issues = collections.defaultdict(list)

    total_files = len(jsonl_files)
    total_pairs = 0
    total_errors = 0
    total_warnings = 0

    # Per-file stats for console output
    file_stats = []  # list of (rel_path, n_pairs, n_errors, n_warnings)

    # Process files
    for file_path in jsonl_files:
        file_pairs = 0
        try:
            file_pairs = len(
                [l for l in file_path.read_text("utf-8").splitlines() if l.strip()]
            )
        except Exception:
            pass  # Counted as error during review anyway
        total_pairs += file_pairs

        rel_path = (
            file_path.relative_to(target_dir) if target_dir.is_dir() else file_path.name
        )
        issues = review_file(file_path, seen_pairs)

        file_errors = 0
        file_warnings = 0
        if issues:
            all_issues[rel_path] = issues
            for _, results in issues:
                for r in results:
                    if r.level.startswith("🔴"):
                        file_errors += 1
                    else:
                        file_warnings += 1

        total_errors += file_errors
        total_warnings += file_warnings
        file_stats.append((str(rel_path), file_pairs, file_errors, file_warnings))

    # Print per-file console output
    if file_stats:
        name_width = max(len(s[0]) for s in file_stats)
        for name, pairs, errs, warns in file_stats:
            parts = [f"  {name:<{name_width}}  {pairs:>4} pairs"]
            if errs:
                parts.append(f"  {errs} error{'s' if errs != 1 else ''}")
            if warns:
                parts.append(f"  {warns} warning{'s' if warns != 1 else ''}")
            print("".join(parts))

        print(f"  {'─' * (name_width + 30)}")
        print(
            f"  Summary: {total_files} files, {total_pairs} pairs, "
            f"{total_errors} error{'s' if total_errors != 1 else ''}, "
            f"{total_warnings} warning{'s' if total_warnings != 1 else ''}"
        )

    # Generate report
    out_report.parent.mkdir(parents=True, exist_ok=True)

    report = [
        f"# Corpus Review Report\n",
        f"**Target:** `{target_dir}`\n",
        f"**Files scanned:** {total_files}",
        f"**Total pairs:** {total_pairs}\n",
        f"## Summary\n",
        f"- 🔴 **Errors:** {total_errors}",
        f"- 🟡 **Warnings:** {total_warnings}\n",
    ]

    if not all_issues:
        report.append("🎉 **All clear!** No issues found in the corpus.")
    else:
        report.append("## Detailed Findings\n")

        for rel_path in sorted(all_issues.keys()):
            report.append(f"### 📄 `{rel_path}`\n")
            report.append("| Line | Level | Rule | Message | Breton | Français |")
            report.append("|------|-------|------|---------|--------|----------|")

            for line_num, results in all_issues[rel_path]:
                for res in results:

                    def safe(v):
                        sv = str(v).replace("|", "\\|").replace("\n", " ")
                        return sv[:97] + "..." if len(sv) > 100 else sv

                    s_br = safe(res.breton)
                    s_fr = safe(res.francais)
                    report.append(
                        f"| {line_num} | {res.level} | **{res.rule}** | {res.message} | `{s_br}` | `{s_fr}` |"
                    )
            report.append("")  # Empty line after table

    out_report.write_text("\n".join(report), encoding="utf-8")
    print(f"  ✅ Report: {out_report}")


def main(argv=None):
    """Entry point. Pass argv list for programmatic use, or None for CLI."""
    parser = argparse.ArgumentParser(
        description="Quality assurance on extracted JSONL corpus.",
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Book folder(s) in ocr/, or arbitrary paths to .jsonl files/directories. Default: all books in ocr/.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Specific model subfolder to target (e.g. antigravity).",
    )
    args = parser.parse_args(argv)

    targets_to_process = []  # list of (target_path, report_path)

    if args.targets:
        for t in args.targets:
            p = Path(t)
            # If it's a direct path that exists
            if p.exists():
                if p.is_file() and p.suffix == ".jsonl":
                    parent = p.parent
                    try:
                        rel = parent.resolve().relative_to(OCR_DIR.resolve())
                        report_path = REPORTS_DIR / rel / f"{p.stem}_review.md"
                    except ValueError:
                        report_path = parent / f"{p.stem}_review.md"
                    targets_to_process.append((p, report_path))
                elif p.is_dir():
                    try:
                        rel = p.resolve().relative_to(OCR_DIR.resolve())
                        report_path = REPORTS_DIR / rel / "review.md"
                    except ValueError:
                        report_path = p / "review.md"
                    targets_to_process.append((p, report_path))
            else:
                # Treat as a book name inside ocr/
                book_dir = OCR_DIR / t
                if book_dir.exists() and book_dir.is_dir():
                    models = (
                        [args.model]
                        if args.model
                        else [d.name for d in book_dir.iterdir() if d.is_dir()]
                    )
                    for model in models:
                        model_dir = book_dir / model
                        if model_dir.exists() and model_dir.is_dir():
                            report_path = REPORTS_DIR / t / model / "review.md"
                            targets_to_process.append((model_dir, report_path))
                else:
                    print(
                        f"❌ Target not found: {t} (neither a direct path nor a known book in ocr/)",
                        file=sys.stderr,
                    )
    else:
        # Default: all books in ocr directory
        if OCR_DIR.exists():
            for book_dir in [d for d in OCR_DIR.iterdir() if d.is_dir()]:
                models = (
                    [args.model]
                    if args.model
                    else [d.name for d in book_dir.iterdir() if d.is_dir()]
                )
                for model in models:
                    model_dir = book_dir / model
                    if model_dir.exists() and model_dir.is_dir():
                        report_path = REPORTS_DIR / book_dir.name / model / "review.md"
                        targets_to_process.append((model_dir, report_path))

    if not targets_to_process:
        print("ℹ️ No valid targets found to review.", file=sys.stderr)
        return

    for target_path, report_path in targets_to_process:
        review_target(target_path, report_path)


if __name__ == "__main__":
    main()
