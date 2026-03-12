#!/usr/bin/env python3
"""
Gemini Batch API support for whole-book OCR.

Submits all pages of a book as a single batch job to the Gemini Batch API,
which processes them asynchronously at 50% of the standard cost.

Three-phase workflow:
  1. submit  — upload images + create batch job
  2. status  — poll job state
  3. collect — retrieve results and write JSONL + report

Each batch run is stored in its own timestamped folder:
  ocr/<book>/<model>/batch-YYYYMMDD-HHMM/
    ├── batch_state.json   — job metadata + submitted page list
    ├── prompt.md          — full prompt snapshot
    ├── corpus/            — per-page JSONL files
    └── reports/           — quality report

Requires:
  pip install google-genai
  export GEMINI_API_KEY='...'
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import google.genai as genai
    from google.genai import types as genai_types
except ImportError:
    genai = None
    genai_types = None

from scripts.ocr import (
    DEFAULT_MODEL,
    SINGLE_IMAGE_PROMPT,
    MODEL_PRICING,
    detect_provider,
    estimate_cost,
    get_book_prompt,
    get_workflow_prompt,
    parse_vlm_response,
    write_rapport,
)
from scripts.utils import (
    ReportRow,
    discover_images,
    discover_targets,
    format_cost,
    load_droplist,
    mime_type_for_image,
    should_drop_page,
    write_jsonl,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_FILENAME = "batch_state.json"

# ── Batch cost multiplier (50% discount) ──────────────────────────
BATCH_DISCOUNT = 0.5


def _require_gemini():
    """Ensure the google-genai package is available."""
    if genai is None:
        print(
            "❌ google-genai package not installed. Run: pip install google-genai",
            file=sys.stderr,
        )
        sys.exit(1)


def _create_client():
    """Create a Gemini client, ensuring the API key is set."""
    _require_gemini()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY non définie.", file=sys.stderr)
        sys.exit(1)
    return genai.Client(api_key=api_key)


# ── Batch directory helpers ──────────────────────────────────────


def _make_batch_dirname() -> str:
    """Generate a batch folder name: batch-YYYYMMDD-HHMM."""
    now = datetime.now(timezone.utc)
    return f"batch-{now.strftime('%Y%m%d-%H%M')}"


def find_pending_batch_dirs(model_dir: Path) -> list[Path]:
    """Find all batch-* subdirectories with a pending batch_state.json.

    A batch is 'pending' if the state file exists and status is not 'completed'.
    """
    if not model_dir.exists():
        return []
    pending = []
    for d in sorted(model_dir.iterdir()):
        if not d.is_dir() or not d.name.startswith("batch-"):
            continue
        state_path = d / STATE_FILENAME
        if not state_path.exists():
            continue
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            if state.get("status") != "completed":
                pending.append(d)
        except (json.JSONDecodeError, OSError):
            continue
    return pending


def _load_state(batch_dir: Path) -> dict | None:
    p = batch_dir / STATE_FILENAME
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _save_state(batch_dir: Path, state: dict) -> None:
    batch_dir.mkdir(parents=True, exist_ok=True)
    (batch_dir / STATE_FILENAME).write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# ── File API helpers ─────────────────────────────────────────────


def _build_display_name(book: str, page_stem: str) -> str:
    """Build a unique display_name for a page upload: 'ocr/<book>/<page>'."""
    return f"ocr/{book}/{page_stem}"


def _list_existing_uploads(client) -> dict[str, object]:
    """Return a dict mapping display_name → file object for all uploaded files."""
    existing = {}
    for f in client.files.list():
        if f.display_name:
            existing[f.display_name] = f
    return existing


def _upload_images(
    client,
    images: list[Path],
    book: str,
    existing_uploads: dict[str, object],
) -> dict[str, object]:
    """Upload page images to the Gemini File API, skipping already-uploaded ones.

    Returns a dict mapping page stem (e.g. '001') → file object.
    """
    uploaded = {}
    for i, img in enumerate(images, 1):
        display_name = _build_display_name(book, img.stem)

        # Check if already uploaded
        if display_name in existing_uploads:
            f = existing_uploads[display_name]
            # File objects have a .state enum; default to ACTIVE if attribute missing
            file_state = getattr(f, "state", None)
            state_name = file_state.name if file_state else "ACTIVE"
            if state_name == "ACTIVE":
                print(f"  ⏭️  [{i}/{len(images)}] {img.name} — already uploaded")
                uploaded[img.stem] = f
                continue

        print(f"  📤 [{i}/{len(images)}] Uploading {img.name}...")
        f = client.files.upload(
            file=str(img),
            config=genai_types.UploadFileConfig(
                display_name=display_name,
                mime_type=mime_type_for_image(img),
            ),
        )
        uploaded[img.stem] = f

    return uploaded


# ── Submit ───────────────────────────────────────────────────────


def submit_batch_job(
    book_dir: Path,
    model: str = DEFAULT_MODEL,
    ocr_root: Path | None = None,
    limit: int | None = None,
    debug: bool = False,
) -> str | None:
    """Submit a whole book as a Gemini Batch API job.

    Returns the batch job name, or None if there's nothing to process.
    """
    # Validate provider
    provider = detect_provider(model)
    if provider != "google":
        print(
            f"❌ Batch mode only supports Gemini models, got '{model}' (provider: {provider})",
            file=sys.stderr,
        )
        sys.exit(1)

    client = _create_client()
    book = book_dir.name

    if ocr_root is None:
        ocr_root = PROJECT_ROOT / "ocr"
    model_dir = ocr_root / book / model

    # Check for existing pending batch job
    pending = find_pending_batch_dirs(model_dir)
    if pending:
        batch_dir = pending[0]
        state = _load_state(batch_dir)
        job_name = state.get("job_name", "?") if state else "?"
        print(f"⚠️  A batch job is already pending for {book}/{model}:")
        print(f"   Folder: {batch_dir.name}")
        print(f"   Job: {job_name}")
        print(f"   Use 'pipeline.py batch_status {book}' to check/collect results.")
        return None

    # Discover images
    images = discover_images(book_dir)
    if not images:
        print(f"  ⚠️  No images found in {book_dir}/")
        return None

    # Filter droplisted pages
    drop_pages = load_droplist(book)
    if drop_pages:
        before = len(images)
        images = [img for img in images if not should_drop_page(img, drop_pages)]
        skipped = before - len(images)
        if skipped:
            print(f"  ⏭️  {skipped} pages in droplist, skipping")

    total_pages = len(images)
    to_process = list(images)

    # Apply --limit
    if limit and limit < len(to_process):
        import random

        to_process = sorted(random.sample(to_process, limit), key=lambda p: p.name)
        print(f"  🎲 Random sample of {limit} pages from {total_pages}")

    if not to_process:
        print("  ✅ No pages to process.")
        return None

    print(f"\n📦 Batch submission for {book}")
    print(f"   Model: {model}")
    print(f"   Pages to process: {len(to_process)} / {total_pages}")

    # Phase 1: Upload images
    print(f"\n📤 Phase 1: Uploading {len(to_process)} images to Gemini File API...")
    existing_uploads = _list_existing_uploads(client)
    uploaded_files = _upload_images(client, to_process, book, existing_uploads)
    print(f"   ✅ {len(uploaded_files)} images ready")

    # Phase 2: Build batch requests
    print("\n📝 Phase 2: Building batch requests...")
    global_prompt = get_workflow_prompt()
    book_prompt = get_book_prompt(book)
    system_prompt = global_prompt + book_prompt

    inline_requests = []
    page_key_map = {}  # Maps request index → page stem
    page_extensions = {}  # Maps page stem → file extension (e.g. '.jpg')
    submitted_pages = []  # Ordered list for consistency check

    for idx, img in enumerate(to_process):
        page_stem = img.stem
        file_obj = uploaded_files[page_stem]
        user_text = SINGLE_IMAGE_PROMPT.format(filename=img.name)

        request = {
            "contents": [
                {
                    "parts": [
                        {
                            "file_data": {
                                "file_uri": file_obj.uri,
                                "mime_type": mime_type_for_image(img),
                            }
                        },
                        {"text": user_text},
                    ],
                    "role": "user",
                }
            ],
            "config": {
                "system_instruction": {"parts": [{"text": system_prompt}]},
                "temperature": 0,
            },
        }
        inline_requests.append(request)
        page_key_map[str(idx)] = page_stem
        page_extensions[page_stem] = img.suffix
        submitted_pages.append(page_stem)

    # Phase 3: Submit batch job
    print(f"\n🚀 Phase 3: Submitting batch job ({len(inline_requests)} requests)...")
    batch_job = client.batches.create(
        model=model,
        src=inline_requests,
        config={
            "display_name": f"ocr-{book}-{model}",
        },
    )

    job_name = batch_job.name
    print(f"   ✅ Job created: {job_name}")

    # Rough ballpark estimate (actual cost is computed from real usage at collect time)
    # Images typically use ~1000 input tokens each, VLM responses ~500 output tokens
    est_input_tokens = len(to_process) * 1000
    est_output_tokens = len(to_process) * 500
    est_cost = estimate_cost(model, est_input_tokens, est_output_tokens)
    if est_cost is not None:
        batch_cost = est_cost * BATCH_DISCOUNT
        print(f"   💰 Estimated cost: ~{format_cost(batch_cost)} (50% batch discount)")

    # Create batch directory
    batch_dirname = _make_batch_dirname()
    batch_dir = model_dir / batch_dirname
    corpus_dir = batch_dir / "corpus"
    reports_dir = batch_dir / "reports"
    corpus_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Write prompt snapshot
    prompt_path = batch_dir / "prompt.md"
    prompt_content = f"# Prompt Snapshot\n\n"
    prompt_content += f"**Model**: {model}\n"
    prompt_content += f"**Book**: {book}\n"
    prompt_content += f"**Date**: {datetime.now(timezone.utc).isoformat()}\n\n"
    prompt_content += f"## System Prompt (global)\n\n{global_prompt}\n\n"
    if book_prompt:
        prompt_content += f"## Book-specific Prompt\n\n{book_prompt}\n\n"
    prompt_content += f"## User Prompt Template\n\n```\n{SINGLE_IMAGE_PROMPT}\n```\n"
    prompt_path.write_text(prompt_content, encoding="utf-8")

    # Save state
    state = {
        "status": "pending",
        "job_name": job_name,
        "model": model,
        "book": book,
        "batch_dir": batch_dirname,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "total_pages": total_pages,
        "submitted_pages": submitted_pages,
        "page_key_map": page_key_map,
        "page_extensions": page_extensions,
        "uploaded_files": {
            stem: {"name": f.name, "uri": f.uri} for stem, f in uploaded_files.items()
        },
    }
    _save_state(batch_dir, state)
    print(f"   📄 Batch folder: {batch_dir}")

    print(
        f"\n✅ Batch job submitted. Use 'pipeline.py batch_status {book}' to check progress."
    )
    return job_name


# ── Status / Poll ────────────────────────────────────────────────


def check_batch_status(
    book: str,
    model: str = DEFAULT_MODEL,
    ocr_root: Path | None = None,
    wait: bool = False,
    cancel: bool = False,
    poll_interval: int = 30,
) -> str | None:
    """Check the status of a batch job, optionally waiting for completion.

    Returns the final job state name, or None if no job found.
    """
    client = _create_client()

    if ocr_root is None:
        ocr_root = PROJECT_ROOT / "ocr"
    model_dir = ocr_root / book / model

    pending = find_pending_batch_dirs(model_dir)
    if not pending:
        print(f"  ⚠️  No pending batch job found for {book}/{model}")
        return None

    # Process the most recent pending batch
    batch_dir = pending[-1]
    state = _load_state(batch_dir)
    if not state:
        print(f"  ⚠️  Could not read state from {batch_dir}")
        return None

    job_name = state["job_name"]
    print(f"📋 Batch job: {job_name}")
    print(f"   Folder: {batch_dir.name}")
    print(f"   Book: {state['book']}")
    print(f"   Model: {state['model']}")
    print(f"   Submitted: {state['submitted_at']}")
    print(
        f"   Pages: {len(state.get('submitted_pages', state.get('page_key_map', {})))}"
    )

    # Cancel if requested
    if cancel:
        print(f"\n⛔ Cancelling job {job_name}...")
        client.batches.cancel(name=job_name)
        print("   ✅ Cancel request sent")
        state["status"] = "cancelled"
        _save_state(batch_dir, state)
        return "JOB_STATE_CANCELLED"

    # Poll
    completed_states = {
        "JOB_STATE_SUCCEEDED",
        "JOB_STATE_FAILED",
        "JOB_STATE_CANCELLED",
        "JOB_STATE_EXPIRED",
    }

    batch_job = client.batches.get(name=job_name)
    job_state = batch_job.state.name

    if job_state in completed_states:
        print(f"\n   State: {job_state}")
        if job_state == "JOB_STATE_SUCCEEDED":
            print("\n🎉 Job completed! Collecting results...")
            _collect_results(client, batch_job, state, batch_dir)
        else:
            if job_state == "JOB_STATE_FAILED":
                print(f"   Error: {batch_job.error}")
            state["status"] = job_state.lower()
            _save_state(batch_dir, state)
        return job_state

    if not wait:
        print(f"\n   State: {job_state}")
        print(f"   Run 'pipeline.py batch_status {book} --wait' to poll until done.")
        return job_state

    # Polling loop
    print(f"\n⏳ Waiting for job to complete (polling every {poll_interval}s)...")
    while job_state not in completed_states:
        print(f"   [{datetime.now().strftime('%H:%M:%S')}] {job_state}")
        time.sleep(poll_interval)
        batch_job = client.batches.get(name=job_name)
        job_state = batch_job.state.name

    print(f"\n   Final state: {job_state}")
    if job_state == "JOB_STATE_SUCCEEDED":
        print("\n🎉 Job completed! Collecting results...")
        _collect_results(client, batch_job, state, batch_dir)
    else:
        if job_state == "JOB_STATE_FAILED":
            print(f"   Error: {batch_job.error}")
        state["status"] = job_state.lower()
        _save_state(batch_dir, state)

    return job_state


# ── Collect ──────────────────────────────────────────────────────


def _collect_results(
    client,
    batch_job,
    state: dict,
    batch_dir: Path,
) -> None:
    """Collect results from a completed batch job, write JSONL + report."""
    book = state["book"]
    model = state["model"]
    page_key_map = state["page_key_map"]
    page_extensions = state.get("page_extensions", {})
    submitted_pages = state.get("submitted_pages", list(page_key_map.values()))
    total_pages = state.get("total_pages", len(page_key_map))

    corpus_dir = batch_dir / "corpus"
    reports_dir = batch_dir / "reports"
    corpus_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    rapport_path = reports_dir / "report.md"

    # Load existing report rows if any
    from scripts.ocr import load_rapport

    rows, observations = load_rapport(rapport_path)

    # Collect inline responses
    if batch_job.dest and batch_job.dest.inlined_responses:
        responses = batch_job.dest.inlined_responses
        print(f"   Processing {len(responses)} responses...")

        # Consistency check
        if len(responses) != len(submitted_pages):
            print(
                f"   ⚠️  Response count ({len(responses)}) != submitted pages ({len(submitted_pages)})",
                file=sys.stderr,
            )

        for idx, inline_response in enumerate(responses):
            page_stem = page_key_map.get(str(idx))
            if not page_stem:
                print(
                    f"   ⚠️  No page mapping for response index {idx}", file=sys.stderr
                )
                continue

            ext = page_extensions.get(page_stem, ".png")
            page_name = f"{page_stem}{ext}"
            jsonl_path = corpus_dir / f"{page_stem}.jsonl"

            if inline_response.response:
                text = ""
                try:
                    text = inline_response.response.text or ""
                except AttributeError:
                    text = str(inline_response.response)

                # Parse the VLM response
                parsed = parse_vlm_response(text)

                # Get usage metadata
                usage = getattr(inline_response.response, "usage_metadata", None)
                prompt_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
                completion_tokens = (
                    getattr(usage, "candidates_token_count", 0) if usage else 0
                )
                cost = estimate_cost(model, prompt_tokens, completion_tokens)
                if cost is not None:
                    cost *= BATCH_DISCOUNT  # Apply batch discount

                # Write JSONL
                n_pairs = write_jsonl(jsonl_path, parsed["jsonl"])
                cost_str = format_cost(cost)
                print(f"   ✅ {page_name} → {n_pairs} pairs  💰 {cost_str}")

                rows.append(
                    ReportRow(
                        image=page_name,
                        pairs=str(n_pairs),
                        statut=parsed["statut"],
                        score=parsed["score"],
                        time="batch",
                        cost=cost_str,
                        remarques=parsed["remarques"],
                    )
                )

                if (
                    parsed["observations"]
                    and parsed["observations"].lower() != "aucune"
                ):
                    observations.append(f"[{page_name}] {parsed['observations']}")

            elif inline_response.error:
                err_msg = str(inline_response.error)
                print(f"   ❌ {page_name}: {err_msg[:80]}", file=sys.stderr)
                # Create empty file for resumability
                jsonl_path.touch()
                rows.append(
                    ReportRow(
                        image=page_name,
                        pairs="0",
                        statut="Erreur",
                        score="N/A",
                        time="",
                        cost="",
                        remarques=err_msg[:80],
                    )
                )
            else:
                print(f"   ⚠️  {page_name}: No response or error", file=sys.stderr)
                jsonl_path.touch()

    # If results came as a file
    elif batch_job.dest and batch_job.dest.file_name:
        result_file_name = batch_job.dest.file_name
        print(f"   Downloading results file: {result_file_name}")
        file_content = client.files.download(file=result_file_name)
        content_str = file_content.decode("utf-8")

        for line_idx, line in enumerate(content_str.strip().splitlines()):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                print(f"   ⚠️  Malformed JSON at line {line_idx}", file=sys.stderr)
                continue

            page_stem = page_key_map.get(str(line_idx))
            if not page_stem:
                continue

            ext = page_extensions.get(page_stem, ".png")
            page_name = f"{page_stem}{ext}"
            jsonl_path = corpus_dir / f"{page_stem}.jsonl"

            # The response structure from file-based output
            resp_text = ""
            if "response" in entry:
                candidates = entry["response"].get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    resp_text = "".join(p.get("text", "") for p in parts)

            if resp_text:
                parsed = parse_vlm_response(resp_text)
                n_pairs = write_jsonl(jsonl_path, parsed["jsonl"])
                print(f"   ✅ {page_name} → {n_pairs} pairs")

                rows.append(
                    ReportRow(
                        image=page_name,
                        pairs=str(n_pairs),
                        statut=parsed["statut"],
                        score=parsed["score"],
                        time="batch",
                        cost="",
                        remarques=parsed["remarques"],
                    )
                )
            else:
                jsonl_path.touch()
    else:
        print("   ⚠️  No results found in batch job response.")

    # Write report
    write_rapport(
        rapport_path,
        rows,
        observations,
        model=model,
        total_pages=total_pages,
        book_name=book,
    )
    print(f"\n   📊 Report: {rapport_path}")

    # Mark state as completed (keep file for auditability)
    state["status"] = "completed"
    state["completed_at"] = datetime.now(timezone.utc).isoformat()
    _save_state(batch_dir, state)
    print(f"   ✅ Batch completed: {batch_dir.name}")


# ── CLI ──────────────────────────────────────────────────────────


def main(argv=None):
    """Entry point for batch OCR operations."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Gemini Batch API for whole-book OCR",
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    # --- submit ---
    p_submit = subparsers.add_parser("submit", help="Submit a batch OCR job")
    p_submit.add_argument(
        "targets",
        nargs="*",
        help="Book folder(s) under pages_enhanced/ (default: all)",
    )
    p_submit.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini model (default: {DEFAULT_MODEL})",
    )
    p_submit.add_argument(
        "-o", "--output", type=Path, default=None, help="Output root directory"
    )
    p_submit.add_argument(
        "--limit", type=int, default=None, help="Process only N random pages"
    )
    p_submit.add_argument("--debug", action="store_true", default=False)

    # --- status ---
    p_status = subparsers.add_parser(
        "status", help="Check batch job status / collect results"
    )
    p_status.add_argument(
        "targets",
        nargs="*",
        help="Book folder(s) to check (default: all with pending jobs)",
    )
    p_status.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model subfolder (default: {DEFAULT_MODEL})",
    )
    p_status.add_argument(
        "-o", "--output", type=Path, default=None, help="OCR root directory"
    )
    p_status.add_argument(
        "--wait", action="store_true", help="Poll until job completes"
    )
    p_status.add_argument(
        "--cancel", action="store_true", help="Cancel the running job"
    )

    args = parser.parse_args(argv)
    pages_dir = PROJECT_ROOT / "pages_enhanced"
    ocr_root = args.output if args.output else PROJECT_ROOT / "ocr"

    if args.action == "submit":
        book_dirs, _ = discover_targets(args.targets or None, pages_dir)
        if not book_dirs:
            print(f"Aucun livre trouvé dans {pages_dir.absolute()}")
            sys.exit(1)

        for book_dir in book_dirs:
            submit_batch_job(
                book_dir,
                model=args.model,
                ocr_root=ocr_root,
                limit=args.limit,
                debug=args.debug,
            )

    elif args.action == "status":
        if args.targets:
            books = args.targets
        else:
            # Auto-discover books with pending batch jobs
            books = []
            if ocr_root.exists():
                for book_dir in sorted(ocr_root.iterdir()):
                    if not book_dir.is_dir():
                        continue
                    model_dir = book_dir / args.model
                    if find_pending_batch_dirs(model_dir):
                        books.append(book_dir.name)
            if not books:
                print("  No pending batch jobs found.")
                return

        for book in books:
            print(f"\n{'─' * 60}")
            check_batch_status(
                book,
                model=args.model,
                ocr_root=ocr_root,
                wait=args.wait,
                cancel=args.cancel,
            )


if __name__ == "__main__":
    main()
