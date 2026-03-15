"""
Core OCR infrastructure — constants, types, and run-folder management.

Shared by providers.py, reports.py, sync.py, and batch.py.

Contains:
- Constants (MODEL_PRICING, DEFAULT_MODEL, MAX_COMPLETION_TOKENS, SINGLE_IMAGE_PROMPT)
- TypedDicts (ParsedResponse, VLMResult)
- Image encoding
- Prompt loading
- Cost estimation & provider detection
- Response parsing (parse_vlm_response)
- Run-folder management (prompt hashing, folder discovery, state I/O)
"""

import os
import sys
import re
import time
import hashlib
import json
import base64
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

from src.utils import (
    ReportRow,
    compute_summary_stats,
    count_jsonl_pairs,
    discover_images,
    discover_targets,
    format_cost,
    image_sort_key,
    is_auth_error,
    mime_type_for_image,
    safe_float,
    safe_int,
    write_jsonl,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_MODEL = "gemini-3.1-pro-preview"
MAX_COMPLETION_TOKENS = 4000


class ParsedResponse(TypedDict):
    """Structured fields extracted from a VLM response."""

    jsonl: str
    statut: str
    score: str
    remarques: str
    observations: str


class VLMResult(TypedDict):
    """Full result from processing a single image through a VLM."""

    jsonl: str
    statut: str
    score: str
    remarques: str
    observations: str
    raw: str
    elapsed: float
    prompt_tokens: int
    completion_tokens: int
    cost: float | None


# ── Image encoding ──────────────────────────────────────────────


def encode_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ── Prompt loading ──────────────────────────────────────────────


def get_workflow_prompt(path: Path | str | None = None) -> str:
    """Load the main system prompt.

    Args:
        path: Override prompt file path. Default: ``prompts/extract_bilingual_corpus.md``.
    """
    if path is not None:
        return Path(path).read_text(encoding="utf-8")
    return (PROJECT_ROOT / "prompts" / "extract_bilingual_corpus.md").read_text(
        encoding="utf-8"
    )


def get_book_prompt(book_name: str, path: Path | str | None = None) -> str:
    """Load a book-specific prompt.

    Args:
        book_name: Book name (used to auto-detect ``prompts/<book_name>.md``).
        path: Override prompt file path. When given, *replaces* auto-detection.
    """
    if path is not None:
        return "\n\n---\n\n" + Path(path).read_text(encoding="utf-8")
    book_prompt_path = PROJECT_ROOT / "prompts" / f"{book_name}.md"
    if book_prompt_path.exists():
        return "\n\n---\n\n" + book_prompt_path.read_text(encoding="utf-8")
    return ""


SINGLE_IMAGE_PROMPT = """\
Voici l'image : {filename}

Applique strictement le workflow fourni sur cette UNIQUE image.

Structurez votre réponse EXACTEMENT comme suit, en distinguant bien les deux sections :

=== JSONL ===
(uniquement les lignes JSONL, une par paire breton/français, rien d'autre)
=== /JSONL ===

=== RAPPORT ===
Statut: OK | Difficultés | Impossible
Score: <nombre entier entre 0 et 100>
Remarques: <une phrase décrivant les difficultés ou observations>
Observations workflow: <suggestions d'amélioration du workflow si pertinent, sinon "aucune">
=== /RAPPORT ===

Ne mettez RIEN d'autre dans votre réponse.
"""


# ── Cost estimation (per 1M tokens) ──────────────────────────────
# Approximate pricing — update as needed.
MODEL_PRICING = {
    # GPT-5 family
    "gpt-5.2": {"input": 1.75, "output": 14.00},
    "gpt-5.2-pro": {"input": 21.00, "output": 168.00},
    "gpt-5.2-chat-latest": {"input": 1.75, "output": 14.00},
    "gpt-5.1": {"input": 1.25, "output": 10.00},
    "gpt-5.1-chat-latest": {"input": 1.25, "output": 10.00},
    "gpt-5": {"input": 1.25, "output": 10.00},
    "gpt-5-pro": {"input": 15.00, "output": 120.00},
    "gpt-5-chat-latest": {"input": 1.25, "output": 10.00},
    "gpt-5-mini": {"input": 0.25, "output": 2.00},
    "gpt-5-nano": {"input": 0.05, "output": 0.40},
    # Codex
    "gpt-5.3-codex": {"input": 1.75, "output": 14.00},
    "gpt-5.2-codex": {"input": 1.75, "output": 14.00},
    "gpt-5.1-codex-max": {"input": 1.25, "output": 10.00},
    "gpt-5.1-codex": {"input": 1.25, "output": 10.00},
    "gpt-5-codex": {"input": 1.25, "output": 10.00},
    # GPT-4.1 family
    "gpt-4.1": {"input": 2.00, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
    # GPT-4o family
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    # o-series
    "o3": {"input": 2.00, "output": 8.00},
    "o4-mini": {"input": 1.10, "output": 4.40},
    # Anthropic Claude (prices in $/MTok: input / output)
    # — Opus 4.6
    "claude-opus-4-6": {"input": 5.00, "output": 25.00},
    # — Opus 4.5
    "claude-opus-4-5-20251101": {"input": 5.00, "output": 25.00},
    "claude-opus-4.5": {"input": 5.00, "output": 25.00},
    # — Opus 4.1
    "claude-opus-4-1-20250805": {"input": 15.00, "output": 75.00},
    # — Opus 4
    "claude-opus-4-20250514": {"input": 15.00, "output": 75.00},
    "claude-opus-4": {"input": 15.00, "output": 75.00},
    # — Sonnet 4.6
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    # — Sonnet 4.5
    "claude-sonnet-4-5-20250929": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4.5": {"input": 3.00, "output": 15.00},
    # — Sonnet 4
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    # — Haiku 4.5
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "claude-haiku-4.5": {"input": 1.00, "output": 5.00},
    # — Haiku 3.5
    "claude-haiku-3.5": {"input": 0.80, "output": 4.00},
    # Google Gemini
    "gemini-3.1-pro": {"input": 2.00, "output": 12.00},
    "gemini-3.1-pro-preview": {"input": 2.00, "output": 12.00},
    "gemini-3-pro": {"input": 2.00, "output": 12.00},
    "gemini-3-flash": {"input": 0.50, "output": 3.00},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "gemini-2.5-flash": {"input": 0.15, "output": 0.60},
    "gemini-2.5-flash-lite": {"input": 0.10, "output": 0.40},
}


def estimate_cost(
    model: str, prompt_tokens: int, completion_tokens: int
) -> float | None:
    """Estimate API cost in USD. Returns None if model pricing is unknown."""
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        return None
    return (
        prompt_tokens * pricing["input"] + completion_tokens * pricing["output"]
    ) / 1_000_000


# ── Provider detection ─────────────────────────────────────────


def detect_provider(model: str) -> str:
    """Detect API provider from model name. Returns 'anthropic', 'google', or 'openai'."""
    if model.startswith("claude"):
        return "anthropic"
    if model.startswith("gemini"):
        return "google"
    return "openai"


# ── Response parsing ──────────────────────────────────────────


def parse_vlm_response(text: str) -> ParsedResponse:
    """Parse a VLM response into JSONL content and report fields.

    Extracts the === JSONL === and === RAPPORT === blocks from the raw
    model response.  Used by both synchronous and batch OCR paths.
    """
    # --- Parse JSONL ---
    jsonl_match = re.search(r"=== JSONL ===\s*\n(.*?)\n=== /JSONL ===", text, re.DOTALL)
    jsonl_content = jsonl_match.group(1).strip() if jsonl_match else ""

    # --- Parse RAPPORT ---
    rapport_match = re.search(
        r"=== RAPPORT ===\s*\n(.*?)\n=== /RAPPORT ===", text, re.DOTALL
    )
    rapport_block = rapport_match.group(1).strip() if rapport_match else ""

    statut = "Impossible"
    score = "N/A"
    remarques = ""
    observations = ""

    for line in rapport_block.splitlines():
        line = line.strip()
        if line.lower().startswith("statut:"):
            statut = line.split(":", 1)[1].strip()
        elif line.lower().startswith("score:"):
            raw = line.split(":", 1)[1].strip().rstrip("%")
            score = raw
        elif line.lower().startswith("remarques:"):
            remarques = line.split(":", 1)[1].strip()
        elif line.lower().startswith("observations workflow:"):
            observations = line.split(":", 1)[1].strip()

    return {
        "jsonl": jsonl_content,
        "statut": statut,
        "score": score,
        "remarques": remarques,
        "observations": observations,
    }


# ═══════════════════════════════════════════════════════════════
# Run-folder management
# ═══════════════════════════════════════════════════════════════
#
# Unified folder structure for both sync and batch OCR runs:
#
#     ocr/<book>/<model>/<NNNN>-<YYYYMMDD>-<HHMM>/
#     ├── prompt.md            ← full prompt snapshot
#     ├── run_state.json       ← metadata + prompt hash
#     ├── extracted/           ← per-page JSONL
#     └── reports/
#         └── extraction/      ← per-page reports + summary
#
# **Prompt-hash reuse**: if the full prompt text (system + global +
# book) has not changed since the last run, the existing folder is
# reused and processing resumes.  A prompt change triggers a new
# run folder with an incremented counter.

STATE_FILENAME = "run_state.json"
PROMPT_FILENAME = "prompt.md"
EXTRACTED_DIR = "extracted"
REPORTS_EXTRACTION_DIR = "reports/extraction"

# Regex to parse run folder names: NNNN-YYYYMMDD-HHMM
RUN_FOLDER_RE = re.compile(r"^(\d{4})-(\d{8})-(\d{4})$")


def compute_prompt_hash(prompt_text: str) -> str:
    """Compute a short hash of the full prompt text.

    Returns the first 8 hex characters of the SHA-256 digest.
    """
    return hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()[:8]


def _parse_run_number(name: str) -> int | None:
    """Extract the run number from a folder name, or None if invalid."""
    m = RUN_FOLDER_RE.match(name)
    return int(m.group(1)) if m else None


def list_run_folders(model_dir: Path) -> list[Path]:
    """List all valid run folders under a model directory, sorted by number."""
    if not model_dir.exists():
        return []
    folders = []
    for d in model_dir.iterdir():
        if d.is_dir() and RUN_FOLDER_RE.match(d.name):
            folders.append(d)
    return sorted(folders, key=lambda p: p.name)


def next_run_number(model_dir: Path) -> int:
    """Return the next available run number (highest existing + 1)."""
    folders = list_run_folders(model_dir)
    if not folders:
        return 1
    nums = [_parse_run_number(f.name) for f in folders]
    return max(n for n in nums if n is not None) + 1


def latest_run_folder(model_dir: Path) -> Path | None:
    """Return the run folder with the highest number, or None."""
    folders = list_run_folders(model_dir)
    return folders[-1] if folders else None


def load_run_state(run_dir: Path) -> dict | None:
    """Load run_state.json from a run directory."""
    p = run_dir / STATE_FILENAME
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def save_run_state(run_dir: Path, state: dict) -> None:
    """Write run_state.json to a run directory."""
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / STATE_FILENAME).write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _make_run_dirname(number: int) -> str:
    """Generate a run folder name: NNNN-YYYYMMDD-HHMM."""
    now = datetime.now(timezone.utc)
    return f"{number:04d}-{now.strftime('%Y%m%d-%H%M')}"


def find_or_create_run_folder(
    model_dir: Path,
    book: str,
    model: str,
    prompt_text: str,
    *,
    mode: str = "sync",
) -> Path:
    """Find an existing run folder with matching prompt hash, or create a new one.

    When the prompt hash matches an existing folder whose status is not
    'completed', that folder is returned for resuming.  Otherwise a new
    folder is created with an incremented counter.

    Args:
        model_dir: ``ocr/<book>/<model>/`` directory.
        book: Book name.
        model: Model name.
        prompt_text: Full concatenated prompt (system + global + book).
        mode: ``"sync"`` or ``"batch"``.

    Returns:
        Path to the run folder (created if new).
    """
    prompt_hash = compute_prompt_hash(prompt_text)

    # Scan existing folders for a matching prompt hash
    for run_dir in reversed(list_run_folders(model_dir)):
        state = load_run_state(run_dir)
        if state and state.get("prompt_hash") == prompt_hash:
            # Reuse existing folder — even if completed, the caller
            # will detect that all pages are done and skip processing.
            return run_dir

    # No match — create a new folder
    number = next_run_number(model_dir)
    dirname = _make_run_dirname(number)
    run_dir = model_dir / dirname

    # Create directory structure
    (run_dir / EXTRACTED_DIR).mkdir(parents=True, exist_ok=True)
    (run_dir / REPORTS_EXTRACTION_DIR).mkdir(parents=True, exist_ok=True)

    # Write initial state
    state = {
        "prompt_hash": prompt_hash,
        "model": model,
        "book": book,
        "mode": mode,
        "status": "in_progress",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "processed_pages": [],
    }
    save_run_state(run_dir, state)

    # Write full prompt snapshot
    (run_dir / PROMPT_FILENAME).write_text(prompt_text, encoding="utf-8")

    return run_dir


def find_pending_runs(model_dir: Path, *, mode: str = "batch") -> list[Path]:
    """Find run folders with pending jobs of the given mode.

    Returns a list of run directories (may be empty).
    """
    pending = []
    for run_dir in list_run_folders(model_dir):
        state = load_run_state(run_dir)
        if (
            state
            and state.get("mode") == mode
            and state.get("status") in ("submitted", "pending", "in_progress")
        ):
            pending.append(run_dir)
    return pending


# ── Convenience path helpers ─────────────────────────────────────


def extracted_dir(run_dir: Path) -> Path:
    return run_dir / EXTRACTED_DIR


def reports_extraction_dir(run_dir: Path) -> Path:
    return run_dir / REPORTS_EXTRACTION_DIR
