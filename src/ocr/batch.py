"""
Gemini Batch API support for whole-book OCR.

Submits all pages of a book as a single batch job to the Gemini Batch API,
which processes them asynchronously at 50% of the standard cost.

Three-phase workflow:
  1. submit  — upload images + create batch job
  2. status  — poll job state
  3. collect — retrieve results and write JSONL + report
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

from src.ocr.core import (
    DEFAULT_MODEL,
    PROJECT_ROOT,
    SINGLE_IMAGE_PROMPT,
    THINKING_LEVELS,
    compute_prompt_hash,
    detect_provider,
    estimate_cost,
    extracted_dir,
    find_or_create_run_folder,
    find_pending_runs,
    get_book_prompt,
    get_workflow_prompt,
    load_run_state,
    model_dir_name,
    parse_vlm_response,
    reports_extraction_dir,
    save_run_state,
)
from src.ocr.providers import create_client
from src.ocr.reports import load_rapport, write_page_report, write_rapport
from src.utils import (
    ReportRow,
    discover_images,
    discover_targets,
    format_cost,
    load_droplist,
    mime_type_for_image,
    should_drop_page,
    write_jsonl,
)

# ── Batch cost multiplier (50% discount) ──────────────────────────
BATCH_DISCOUNT = 0.5


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
                print(f"  ⏭️  [{i}/{len(images)}] {img.name} — déjà uploadée")
                uploaded[img.stem] = f
                continue

        print(f"  📤 [{i}/{len(images)}] Envoi de {img.name}...")
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
    main_prompt: Path | None = None,
    book_prompt: Path | None = None,
    thinking: str | None = None,
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

    client = create_client("google")
    book = book_dir.name

    if ocr_root is None:
        ocr_root = PROJECT_ROOT / "ocr"
    model_dir = ocr_root / book / model_dir_name(model, thinking)

    # Build the full prompt first (needed for hash)
    global_prompt = get_workflow_prompt(path=main_prompt)
    book_prompt_text = get_book_prompt(book, path=book_prompt)
    system_prompt = global_prompt + book_prompt_text

    # Check for existing pending batch job
    pending = find_pending_runs(model_dir, mode="batch")
    if pending:
        run_dir = pending[0]
        state = load_run_state(run_dir)
        job_name = state.get("job_name", "?") if state else "?"
        print(f"⚠️  Un batch est déjà en cours pour {book}/{model} :")
        print(f"   Dossier : {run_dir.name}")
        print(f"   Job : {job_name}")
        print(f"   Utilisez 'pipeline.py batch_status {book}' pour vérifier/collecter.")
        return None

    # Discover images
    images = discover_images(book_dir)
    if not images:
        print(f"  ⚠️  Aucune image trouvée dans {book_dir}/")
        return None

    # Filter droplisted pages
    drop_pages = load_droplist(book)
    if drop_pages:
        before = len(images)
        images = [img for img in images if not should_drop_page(img, drop_pages)]
        skipped = before - len(images)
        if skipped:
            print(f"  ⏭️  {skipped} pages dans la droplist, ignorées")

    total_pages = len(images)
    to_process = list(images)

    # Apply --limit
    if limit and limit < len(to_process):
        import random

        to_process = sorted(random.sample(to_process, limit), key=lambda p: p.name)
        print(f"  🎲 Échantillon aléatoire de {limit} pages sur {total_pages}")

    if not to_process:
        print("  ✅ Aucune page à traiter.")
        return None

    # Create or reuse run folder
    run_dir = find_or_create_run_folder(
        model_dir,
        book,
        model,
        system_prompt,
        mode="batch",
        thinking=thinking,
    )

    print(f"\n📦 Batch submission for {book}")
    print(f"   Model: {model}")
    print(f"   Run: {run_dir.name}")
    print(f"   Pages to process: {len(to_process)} / {total_pages}")

    # Phase 1: Upload images
    print(f"\n📤 Phase 1: Uploading {len(to_process)} images to Gemini File API...")
    existing_uploads = _list_existing_uploads(client)
    uploaded_files = _upload_images(client, to_process, book, existing_uploads)
    print(f"   ✅ {len(uploaded_files)} images ready")

    # Phase 2: Build batch requests
    print("\n📝 Phase 2: Building batch requests...")

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

        # Add thinking config to batch request if specified
        if thinking and thinking != "default":
            if thinking == "off":
                request["config"]["thinking_config"] = {"thinking_budget": 0}
            else:
                level_name = THINKING_LEVELS.get(thinking)
                if level_name:
                    request["config"]["thinking_config"] = {
                        "thinking_level": level_name
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

    # Rough ballpark estimate
    est_input_tokens = len(to_process) * 1000
    est_output_tokens = len(to_process) * 500
    est_cost = estimate_cost(model, est_input_tokens, est_output_tokens)
    if est_cost is not None:
        batch_cost = est_cost * BATCH_DISCOUNT
        print(f"   💰 Estimated cost: ~{format_cost(batch_cost)} (50% batch discount)")

    # Ensure subdirectories exist
    ext_dir = extracted_dir(run_dir)
    rep_dir = reports_extraction_dir(run_dir)
    ext_dir.mkdir(parents=True, exist_ok=True)
    rep_dir.mkdir(parents=True, exist_ok=True)

    # Save state
    state = load_run_state(run_dir) or {}
    state.update(
        {
            "status": "pending",
            "mode": "batch",
            "job_name": job_name,
            "model": model,
            "book": book,
            "prompt_hash": compute_prompt_hash(system_prompt, thinking=thinking),
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "total_pages": total_pages,
            "submitted_pages": submitted_pages,
            "page_key_map": page_key_map,
            "page_extensions": page_extensions,
            "uploaded_files": {
                stem: {"name": f.name, "uri": f.uri}
                for stem, f in uploaded_files.items()
            },
        }
    )
    save_run_state(run_dir, state)
    print(f"   📄 Run folder: {run_dir}")

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
    thinking: str | None = None,
) -> str | None:
    """Check the status of a batch job, optionally waiting for completion.

    Returns the final job state name, or None if no job found.
    """
    client = create_client("google")

    if ocr_root is None:
        ocr_root = PROJECT_ROOT / "ocr"
    model_dir = ocr_root / book / model_dir_name(model, thinking)

    pending = find_pending_runs(model_dir, mode="batch")
    if not pending:
        print(f"  ⚠️  No pending batch job found for {book}/{model}")
        return None

    # Process the most recent pending run
    run_dir = pending[-1]
    state = load_run_state(run_dir)
    if not state:
        print(f"  ⚠️  Could not read state from {run_dir}")
        return None

    job_name = state["job_name"]
    print(f"📋 Batch job: {job_name}")
    print(f"   Folder: {run_dir.name}")
    print(f"   Book: {state['book']}")
    print(f"   Model: {state['model']}")
    print(f"   Submitted: {state.get('submitted_at', 'N/A')}")
    print(
        f"   Pages: {len(state.get('submitted_pages', state.get('page_key_map', {})))}"
    )

    # Cancel if requested
    if cancel:
        print(f"\n⛔ Cancelling job {job_name}...")
        client.batches.cancel(name=job_name)
        print("   ✅ Cancel request sent")
        state["status"] = "cancelled"
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        save_run_state(run_dir, state)
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
            _collect_results(client, batch_job, state, run_dir)
        else:
            if job_state == "JOB_STATE_FAILED":
                print(f"   Error: {batch_job.error}")
            state["status"] = job_state.lower()
            state["updated_at"] = datetime.now(timezone.utc).isoformat()
            save_run_state(run_dir, state)
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
        _collect_results(client, batch_job, state, run_dir)
    else:
        if job_state == "JOB_STATE_FAILED":
            print(f"   Error: {batch_job.error}")
        state["status"] = job_state.lower()
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        save_run_state(run_dir, state)

    return job_state


# ── Collect ──────────────────────────────────────────────────────


def _collect_results(
    client,
    batch_job,
    state: dict,
    run_dir: Path,
) -> None:
    """Collect results from a completed batch job, write JSONL + report."""
    book = state["book"]
    model = state["model"]
    page_key_map = state["page_key_map"]
    page_extensions = state.get("page_extensions", {})
    submitted_pages = state.get("submitted_pages", list(page_key_map.values()))
    total_pages = state.get("total_pages", len(page_key_map))

    ext_dir = extracted_dir(run_dir)
    rep_dir = reports_extraction_dir(run_dir)
    ext_dir.mkdir(parents=True, exist_ok=True)
    rep_dir.mkdir(parents=True, exist_ok=True)

    rapport_path = rep_dir / "report.md"

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
            jsonl_path = ext_dir / f"{page_stem}.jsonl"

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

                # Write per-page report
                page_result = {
                    "statut": parsed["statut"],
                    "score": parsed["score"],
                    "elapsed": "batch",
                    "cost": cost,
                    "remarques": parsed["remarques"],
                    "observations": parsed.get("observations", ""),
                }
                write_page_report(rep_dir, page_name, page_result)

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
            jsonl_path = ext_dir / f"{page_stem}.jsonl"

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

    # Write summary report
    write_rapport(
        rapport_path,
        rows,
        observations,
        model=model,
        total_pages=total_pages,
        book_name=book,
    )
    print(f"\n   📊 Report: {rapport_path}")

    # Mark state as completed
    state["status"] = "completed"
    state["completed_at"] = datetime.now(timezone.utc).isoformat()
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state["processed_pages"] = submitted_pages
    save_run_state(run_dir, state)
    print(f"   ✅ Run completed: {run_dir.name}")


# ── CLI dispatch ────────────────────────────────────────────────


def run_batch(args) -> None:
    """Execute batch OCR based on parsed CLI args from unified __init__.main()."""
    provider = detect_provider(args.model)
    if provider != "google":
        print(
            f"❌ Batch mode only supports Gemini models, got '{args.model}' (provider: {provider})",
            file=sys.stderr,
        )
        sys.exit(1)

    if getattr(args, "seed", None) is not None:
        import random

        random.seed(args.seed)

    pages_dir = PROJECT_ROOT / "pages_enhanced"
    ocr_root = args.output if args.output else PROJECT_ROOT / "ocr"

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
            main_prompt=getattr(args, "main_prompt", None),
            book_prompt=getattr(args, "book_prompt", None),
            thinking=getattr(args, "thinking", None),
        )
