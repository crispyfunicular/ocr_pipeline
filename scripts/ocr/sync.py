"""
Synchronous (page-by-page) OCR processing.

Processes each page image sequentially via the configured VLM provider
(OpenAI, Anthropic, or Google Gemini).
"""

import sys
import random
from datetime import datetime, timezone
from pathlib import Path

from scripts.ocr.core import (
    DEFAULT_MODEL,
    PROJECT_ROOT,
    detect_provider,
    extracted_dir,
    find_or_create_run_folder,
    get_book_prompt,
    get_workflow_prompt,
    load_run_state,
    reports_extraction_dir,
    save_run_state,
)
from scripts.ocr.providers import create_client, process_single_image
from scripts.ocr.reports import load_rapport, write_page_report, write_rapport
from scripts.utils import (
    ReportRow,
    compute_summary_stats,
    discover_images,
    discover_targets,
    format_cost,
    is_auth_error,
    load_droplist,
    should_drop_page,
    write_jsonl,
)

# ── Book processing ─────────────────────────────────────────────


def process_book_ocr(
    client,
    book_dir: Path,
    run_dir: Path,
    workflow: str,
    model: str = DEFAULT_MODEL,
    debug: bool = False,
    limit: int | None = None,
    output_flat: bool = False,
) -> int:
    """Process all images in a single book directory.

    When ``output_flat`` is False (default), writes JSONL to
    ``run_dir/extracted/``, per-page reports to
    ``run_dir/reports/extraction/XX.md``, and a summary report
    to ``run_dir/reports/extraction/report.md``.

    When ``output_flat`` is True (used with ``--output``), writes
    JSONL directly to ``run_dir/`` without subdirectories or reports.

    If limit is set, only process a random sample of N pages.
    Returns the number of images processed.
    """
    images = discover_images(book_dir)
    if not images:
        print(f"  ⚠️  Aucune image trouvée dans {book_dir}/")
        return 0

    # Filter out dropped pages
    drop_pages = load_droplist(book_dir.name)
    if drop_pages:
        before = len(images)
        images = [img for img in images if not should_drop_page(img, drop_pages)]
        skipped = before - len(images)
        if skipped:
            print(f"  ⏭️  {skipped} pages dans la droplist, ignorées")

    total_pages = len(images)
    if output_flat:
        ext_dir = run_dir
        rep_dir = None
        rapport_path = None
    else:
        ext_dir = extracted_dir(run_dir)
        rep_dir = reports_extraction_dir(run_dir)
        ext_dir.mkdir(parents=True, exist_ok=True)
        rep_dir.mkdir(parents=True, exist_ok=True)
        rapport_path = rep_dir / "report.md"

    # Resume: skip if the .jsonl already exists (even if empty)
    to_process = [img for img in images if not (ext_dir / f"{img.stem}.jsonl").exists()]

    # Apply --limit: random sample
    if limit and limit < len(to_process):
        to_process = sorted(random.sample(to_process, limit), key=lambda p: p.name)
        print(f"  🎲 Échantillon aléatoire de {limit} pages sur {total_pages}")
    else:
        print(f"  {len(to_process)} images restantes sur {total_pages}.")

    if not to_process:
        print("  Tout est déjà traité.")
        return 0

    rows, observations = load_rapport(rapport_path) if rapport_path else ([], [])
    provider = detect_provider(model)
    run_state = load_run_state(run_dir) if not output_flat else None

    for i, img in enumerate(to_process, 1):
        print(f"\n  [{i}/{len(to_process)}] Traitement de {img.name}...")
        try:
            result = process_single_image(
                client, img, workflow, model=model, debug=debug
            )

            # Save JSONL
            jsonl_path = ext_dir / f"{img.stem}.jsonl"
            n_pairs = write_jsonl(jsonl_path, result["jsonl"])
            cost_str = format_cost(result["cost"])
            print(
                f"     -> {jsonl_path.name} ({n_pairs} paires)  ⏱ {result['elapsed']}s  💰 {cost_str}"
            )

            # Write per-page report
            if rep_dir:
                write_page_report(rep_dir, img.name, result)

            # Add row to summary report table
            rows.append(
                ReportRow(
                    image=img.name,
                    pairs=str(n_pairs),
                    statut=result["statut"],
                    score=result["score"],
                    time=f"{result['elapsed']}s",
                    cost=cost_str,
                    remarques=result["remarques"],
                )
            )

            # Collect observations
            if result["observations"] and result["observations"].lower() != "aucune":
                observations.append(f"[{img.name}] {result['observations']}")

            # Rewrite summary report after each image (for resumability)
            if rapport_path:
                write_rapport(
                    rapport_path,
                    rows,
                    observations,
                    model=model,
                    total_pages=total_pages,
                    book_name=book_dir.name,
                )

            # Update run state (in memory — written every 10 pages)
            if not output_flat and run_state:
                if img.stem not in run_state.get("processed_pages", []):
                    run_state.setdefault("processed_pages", []).append(img.stem)
                run_state["total_pages"] = total_pages
                run_state["updated_at"] = datetime.now(timezone.utc).isoformat()
                if i % 10 == 0:
                    save_run_state(run_dir, run_state)

        except Exception as e:
            err_msg = str(e)
            print(f"     ERREUR sur {img.name}: {err_msg}", file=sys.stderr)
            if is_auth_error(err_msg):
                key_var = {
                    "anthropic": "ANTHROPIC_API_KEY",
                    "google": "GEMINI_API_KEY",
                }.get(provider, "OPENAI_API_KEY")
                print(
                    f"\n⛔ Erreur d'authentification. Vérifiez votre {key_var}.",
                    file=sys.stderr,
                )
                sys.exit(1)
            # Other errors: create empty file and continue
            (ext_dir / f"{img.stem}.jsonl").touch()
            rows.append(
                ReportRow(
                    image=img.name,
                    pairs="0",
                    statut="Erreur",
                    score="N/A",
                    time="",
                    cost="",
                    remarques=err_msg[:80],
                )
            )
            if rapport_path:
                write_rapport(
                    rapport_path,
                    rows,
                    observations,
                    model=model,
                    total_pages=total_pages,
                    book_name=book_dir.name,
                )

    # Final state flush
    if run_state:
        save_run_state(run_dir, run_state)

    # --- Per-book summary ---
    stats = compute_summary_stats(rows)
    book_name = book_dir.name
    print(
        f"\n  📖 {book_name} — {stats.total_pages} pages · {stats.total_pairs} paires"
        f" · moy {stats.avg_score:.0f}% · ${stats.total_cost:.2f} · {stats.total_time / 60:.1f} min"
    )

    if not output_flat:
        print(f"     Run : {run_dir.resolve()}")

    # Print prompt suggestions if any
    unique_obs = list(dict.fromkeys(observations))
    if unique_obs:
        print(f"\n  💡 Suggestions d'amélioration du prompt ({len(unique_obs)}) :")
        for obs in unique_obs[:10]:  # cap at 10 for stdout
            print(f"     {obs}")
        if len(unique_obs) > 10:
            print(f"     ... et {len(unique_obs) - 10} autres (voir rapport)")

    return len(to_process)


# ── CLI dispatch ────────────────────────────────────────────────


def run_sync(args) -> None:
    """Execute synchronous OCR based on parsed CLI args."""
    if getattr(args, "seed", None) is not None:
        random.seed(args.seed)

    provider = detect_provider(args.model)
    client = create_client(provider)
    pages_dir = PROJECT_ROOT / "pages_enhanced"

    # Default OCR output root: ocr/   (overridden by --output)
    ocr_root = args.output if args.output is not None else PROJECT_ROOT / "ocr"

    workflow = get_workflow_prompt()

    # Smart target detection: separate image files from book directories
    book_dirs, single_images = discover_targets(args.targets, pages_dir)

    if not book_dirs and not single_images:
        print(f"Aucun livre trouvé dans {pages_dir.absolute()}")
        sys.exit(1)

    if book_dirs:
        print(f"📚 {len(book_dirs)} livre(s) à traiter")
    if single_images:
        print(f"🖼️  {len(single_images)} image(s) individuelle(s)")
    print(f"🤖 Modèle : {args.model}")

    total_processed = 0

    # Process full book directories
    for book_dir in book_dirs:
        book_name = book_dir.name
        print(f"\n{'─' * 60}")
        print(f"📖 {book_name}")
        print(f"{'─' * 60}")

        book_workflow = workflow + get_book_prompt(book_name)

        use_flat = args.output is not None
        if use_flat:
            # --output bypasses run-folder structure: write flat JSONL
            run_dir = ocr_root / book_name / args.model
            run_dir.mkdir(parents=True, exist_ok=True)
        else:
            model_dir = ocr_root / book_name / args.model
            run_dir = find_or_create_run_folder(
                model_dir, book_name, args.model, book_workflow, mode="sync"
            )
            print(f"  📂 Run : {run_dir.name}")

        n = process_book_ocr(
            client,
            book_dir,
            run_dir,
            book_workflow,
            model=args.model,
            debug=args.debug,
            limit=args.limit,
            output_flat=use_flat,
        )
        total_processed += n

        # Mark run as completed if all pages done
        if not use_flat:
            state = load_run_state(run_dir)
            if state:
                remaining = [
                    img
                    for img in discover_images(book_dir)
                    if not (extracted_dir(run_dir) / f"{img.stem}.jsonl").exists()
                ]
                if not remaining:
                    state["status"] = "completed"
                    state["updated_at"] = datetime.now(timezone.utc).isoformat()
                    save_run_state(run_dir, state)

    # Process individual images
    for img_path in single_images:
        book_name = img_path.parent.name
        print(f"\n{'─' * 60}")
        print(f"🖼️  {img_path.resolve()}")
        print(f"{'─' * 60}")

        img_workflow = workflow + get_book_prompt(book_name)

        try:
            result = process_single_image(
                client, img_path, img_workflow, model=args.model, debug=args.debug
            )

            # Determine output path for single image
            if args.output is not None:
                if args.output.suffix == ".jsonl":
                    jsonl_path = args.output
                    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    img_ocr_dir = args.output / book_name / args.model
                    img_ocr_dir.mkdir(parents=True, exist_ok=True)
                    jsonl_path = img_ocr_dir / f"{img_path.stem}.jsonl"
            else:
                # Create run-folder structure
                model_dir = ocr_root / book_name / args.model
                run_dir = find_or_create_run_folder(
                    model_dir, book_name, args.model, img_workflow, mode="sync"
                )
                ext_dir = extracted_dir(run_dir)
                ext_dir.mkdir(parents=True, exist_ok=True)
                jsonl_path = ext_dir / f"{img_path.stem}.jsonl"

                # Write per-page report
                rep_dir = reports_extraction_dir(run_dir)
                rep_dir.mkdir(parents=True, exist_ok=True)
                write_page_report(rep_dir, img_path.name, result)

            n_pairs = write_jsonl(jsonl_path, result["jsonl"])
            cost_str = format_cost(result["cost"])
            print(
                f"  -> {jsonl_path.resolve()} ({n_pairs} paires)  ⏱ {result['elapsed']}s  💰 {cost_str}"
            )

            # Print report to stdout
            print(f"  Statut: {result['statut']}  Score: {result['score']}%")
            if result["remarques"]:
                print(f"  Remarques: {result['remarques']}")
            if result["observations"] and result["observations"].lower() != "aucune":
                print(f"  Observations: {result['observations']}")

            total_processed += 1

        except Exception as e:
            err_msg = str(e)
            print(f"  ERREUR: {err_msg}", file=sys.stderr)
            if is_auth_error(err_msg):
                key_var = {
                    "anthropic": "ANTHROPIC_API_KEY",
                    "google": "GEMINI_API_KEY",
                }.get(provider, "OPENAI_API_KEY")
                print(
                    f"\n⛔ Erreur d'authentification. Vérifiez votre {key_var}.",
                    file=sys.stderr,
                )
                sys.exit(1)

    print(f"\n{'═' * 60}")
    print(f"✅ Terminé. {total_processed} image(s) traitée(s).")
    print(f"{'═' * 60}")
