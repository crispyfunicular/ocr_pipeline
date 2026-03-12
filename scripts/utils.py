"""
Shared utilities for the OCR pipeline scripts.

Provides common helpers for parsing, formatting, target discovery,
and typed data structures used across multiple pipeline stages.
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

# ── Constants ────────────────────────────────────────────────────────

IMAGE_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg", ".tiff", ".tif"})


# ── Typed data structures ────────────────────────────────────────────


class ReportRow(TypedDict):
    """A single row in the OCR extraction report table."""

    image: str
    pairs: str
    statut: str
    score: str
    time: str
    cost: str
    remarques: str


@dataclass
class SummaryStats:
    """Aggregated statistics for a set of report rows."""

    total_pages: int
    total_pairs: int
    total_cost: float
    total_time: float
    avg_score: float
    min_score: int
    max_score: int
    n_ok: int
    n_diff: int
    n_imp: int
    n_err: int


# ── Parsing helpers ──────────────────────────────────────────────────


def safe_int(s: object) -> int | None:
    """Parse a string to int, stripping trailing '%'. Returns None on failure."""
    try:
        return int(str(s).rstrip("%"))
    except (ValueError, TypeError):
        return None


def safe_float(s: object) -> float | None:
    """Parse a string to float, stripping leading '$' and trailing 's'. Returns None on failure."""
    try:
        return float(str(s).lstrip("$").rstrip("s"))
    except (ValueError, TypeError):
        return None


def image_sort_key(row: ReportRow) -> int:
    """Sort key: extract leading digits from image filename."""
    m = re.match(r"(\d+)", row["image"])
    return int(m.group(1)) if m else 0


# ── Formatting helpers ───────────────────────────────────────────────


def format_cost(cost: float | None) -> str:
    """Format a cost value as '$X.XXXX' or 'N/A'."""
    return f"${cost:.4f}" if cost is not None else "N/A"


def count_jsonl_pairs(jsonl_content: str) -> int:
    """Count non-empty lines in JSONL content."""
    if not jsonl_content:
        return 0
    return len([line for line in jsonl_content.splitlines() if line.strip()])


def write_jsonl(path: Path, jsonl_content: str) -> int:
    """Write JSONL content to a file. Returns the pair count."""
    content = (jsonl_content + "\n") if jsonl_content else ""
    path.write_text(content, encoding="utf-8")
    return count_jsonl_pairs(jsonl_content)


# ── Statistics ───────────────────────────────────────────────────────


def compute_summary_stats(rows: list[ReportRow]) -> SummaryStats:
    """Compute aggregated statistics from report rows."""
    scores = [s for s in (safe_int(r["score"]) for r in rows) if s is not None]
    pairs_list = [
        s for s in (safe_int(r.get("pairs", "0")) for r in rows) if s is not None
    ]
    total = len(rows)

    return SummaryStats(
        total_pages=total,
        total_pairs=sum(pairs_list),
        total_cost=sum(
            c for c in (safe_float(r.get("cost", "")) for r in rows) if c is not None
        ),
        total_time=sum(
            t for t in (safe_float(r.get("time", "")) for r in rows) if t is not None
        ),
        avg_score=sum(scores) / len(scores) if scores else 0,
        min_score=min(scores) if scores else 0,
        max_score=max(scores) if scores else 0,
        n_ok=sum(1 for r in rows if r["statut"].startswith("OK")),
        n_diff=sum(1 for r in rows if r["statut"].startswith("Difficultés")),
        n_imp=sum(1 for r in rows if r["statut"].startswith("Impossible")),
        n_err=sum(1 for r in rows if r["statut"].startswith("Erreur")),
    )


# ── Error handling ───────────────────────────────────────────────────


def is_auth_error(err_msg: str) -> bool:
    """Check if an error message indicates an authentication failure."""
    return "401" in err_msg or "auth" in err_msg.lower()


# ── Droplist ─────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_droplist(book_name: str) -> set[int]:
    """Load page numbers to skip for a book from droplist/<book>/drop_pages.json.

    Returns an empty set if no droplist exists.
    """
    import json

    drop_file = PROJECT_ROOT / "droplist" / book_name / "drop_pages.json"
    if not drop_file.exists():
        return set()
    try:
        data = json.loads(drop_file.read_text(encoding="utf-8"))
        return {int(p) for p in data}
    except (json.JSONDecodeError, ValueError) as e:
        print(f"  ⚠️  Invalid droplist {drop_file}: {e}", file=sys.stderr)
        return set()


def should_drop_page(img_path: Path, drop_pages: set[int]) -> bool:
    """Check if a page should be skipped based on droplist.

    Extracts the page number from the filename stem (e.g. '17.png' → 17).
    """
    if not drop_pages:
        return False
    try:
        page_num = int(img_path.stem)
        return page_num in drop_pages
    except ValueError:
        return False


# ── Target discovery ─────────────────────────────────────────────────


def discover_targets(
    targets: list[str] | None,
    pages_dir: Path,
) -> tuple[list[Path], list[Path]]:
    """Separate user-supplied targets into book directories and single image files.

    Args:
        targets: User-supplied target names (book folder names, paths to images or directories).
        pages_dir: Default parent directory for book subdirectories.

    Returns:
        (book_dirs, single_images) — two sorted lists of resolved paths.

    Raises:
        SystemExit: If a target is not found.
    """
    single_images: list[Path] = []
    book_dirs: list[Path] = []

    if targets:
        for t in targets:
            p = Path(t)
            if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS:
                single_images.append(p)
            elif (pages_dir / t).is_dir():
                book_dirs.append(pages_dir / t)
            elif p.is_dir():
                book_dirs.append(p)
            else:
                print(
                    f"❌ Target not found: {t} (not a file or book folder)",
                    file=sys.stderr,
                )
                sys.exit(1)
    else:
        book_dirs = sorted(
            d for d in pages_dir.iterdir() if d.is_dir() and not d.name.startswith(".")
        )

    return book_dirs, single_images


def discover_images(directory: Path) -> list[Path]:
    """Find all image files in a directory, sorted by name.

    Uses IMAGE_EXTENSIONS as the source of truth for supported formats.
    Replaces hardcoded ``*.png`` globs throughout the pipeline.
    """
    return sorted(
        p
        for p in directory.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def mime_type_for_image(path: Path) -> str:
    """Return the MIME type string for an image file based on its extension."""
    ext = path.suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
    }.get(ext, "image/png")
