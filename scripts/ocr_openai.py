#!/usr/bin/env python3
"""
Automatic extraction of bilingual Breton-French corpus from scanned book pages.

Sends each page image to a VLM (OpenAI, Anthropic Claude, or Google Gemini),
parses structured JSONL output + quality report.

- Output: corpus/<book>/<model>/<page>.jsonl
- Reports: reports/<book>/<model>/report.md
- Resumable: skips pages whose .jsonl already exists

Requires:
  pip install openai anthropic google-genai
  export OPENAI_API_KEY='...'       # for OpenAI models
  export ANTHROPIC_API_KEY='...'    # for Claude models
  export GEMINI_API_KEY='...'       # for Gemini models
"""

import os
import sys
import re
import time
import random
import base64
from pathlib import Path
from datetime import datetime
from openai import OpenAI

try:
    import anthropic as _anthropic_module
except ImportError:
    _anthropic_module = None

try:
    import google.genai as _genai_module
    from google.genai import types as _genai_types
except ImportError:
    _genai_module = None
    _genai_types = None

from scripts.utils import (
    ReportRow,
    compute_summary_stats,
    count_jsonl_pairs,
    discover_targets,
    format_cost,
    image_sort_key,
    is_auth_error,
    safe_float,
    safe_int,
    write_jsonl,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "gpt-5.2"


def encode_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_workflow_prompt() -> str:
    path = PROJECT_ROOT / "prompts" / "extract_bilingual_corpus.md"
    return path.read_text(encoding="utf-8")


def get_book_prompt(book_name: str) -> str:
    """Load an optional book-specific prompt from prompts/<book_name>.md."""
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


def create_client(provider: str):
    """Create the appropriate API client for the given provider."""
    if provider == "anthropic":
        if _anthropic_module is None:
            print(
                "❌ anthropic package not installed. Run: pip install anthropic",
                file=sys.stderr,
            )
            sys.exit(1)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ ANTHROPIC_API_KEY non définie.", file=sys.stderr)
            sys.exit(1)
        return _anthropic_module.Anthropic(api_key=api_key)
    elif provider == "google":
        if _genai_module is None:
            print(
                "❌ google-genai package not installed. Run: pip install google-genai",
                file=sys.stderr,
            )
            sys.exit(1)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY non définie.", file=sys.stderr)
            sys.exit(1)
        return _genai_module.Client(api_key=api_key)
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY non définie.", file=sys.stderr)
            sys.exit(1)
        return OpenAI(api_key=api_key)


# ── Provider-specific API calls ────────────────────────────────


def _call_openai(client, model: str, workflow: str, user_text: str, b64: str) -> dict:
    """Call OpenAI chat completions API. Returns normalized response dict."""
    messages = [
        {"role": "system", "content": workflow},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_text},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64}",
                        "detail": "high",
                    },
                },
            ],
        },
    ]

    # Try with temperature=0; some models reject it, so retry without
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            max_completion_tokens=4000,
        )
    except Exception as e:
        if "temperature" in str(e).lower():
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=4000,
            )
        else:
            raise

    usage = response.usage
    return {
        "text": response.choices[0].message.content,
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
    }


def _call_anthropic(
    client, model: str, workflow: str, user_text: str, b64: str
) -> dict:
    """Call Anthropic Messages API. Returns normalized response dict."""
    response = client.messages.create(
        model=model,
        system=workflow,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": b64,
                        },
                    },
                    {"type": "text", "text": user_text},
                ],
            }
        ],
        temperature=0,
        max_tokens=4000,
    )

    usage = response.usage
    text = response.content[0].text if response.content else ""
    return {
        "text": text,
        "prompt_tokens": usage.input_tokens if usage else 0,
        "completion_tokens": usage.output_tokens if usage else 0,
    }


def _call_google(client, model: str, workflow: str, user_text: str, b64: str) -> dict:
    """Call Google Gemini API. Returns normalized response dict."""
    image_bytes = base64.b64decode(b64)

    config = _genai_types.GenerateContentConfig(
        system_instruction=workflow,
        temperature=0,
        max_output_tokens=4000,
    )

    response = client.models.generate_content(
        model=model,
        contents=[
            _genai_types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            user_text,
        ],
        config=config,
    )

    usage = response.usage_metadata
    return {
        "text": response.text or "",
        "prompt_tokens": usage.prompt_token_count if usage else 0,
        "completion_tokens": usage.candidates_token_count if usage else 0,
    }


# ── Main processing function ──────────────────────────────────


def process_single_image(
    client,
    img_path: Path,
    workflow: str,
    model: str = DEFAULT_MODEL,
    debug: bool = False,
) -> dict:
    """Send a single image to the VLM and parse the structured response."""
    b64 = encode_image(img_path)
    user_text = SINGLE_IMAGE_PROMPT.format(filename=img_path.name)
    provider = detect_provider(model)

    if debug:
        print(f"\n{'┄' * 60}")
        print(f"  🐛 DEBUG — Provider: {provider}")
        print(f"  🐛 DEBUG — System prompt ({len(workflow)} chars):")
        print(f"{'┄' * 60}")
        print(workflow[:2000])
        if len(workflow) > 2000:
            print(f"  ... ({len(workflow) - 2000} more chars)")
        print(f"{'┄' * 60}")
        print(f"  🐛 DEBUG — User prompt:")
        print(f"{'┄' * 60}")
        print(user_text)
        print(f"  🐛 DEBUG — Image: {img_path} (base64 {len(b64)} chars)")
        print(f"{'┄' * 60}")

    t0 = time.time()

    if provider == "anthropic":
        result = _call_anthropic(client, model, workflow, user_text, b64)
    elif provider == "google":
        result = _call_google(client, model, workflow, user_text, b64)
    else:
        result = _call_openai(client, model, workflow, user_text, b64)

    elapsed = time.time() - t0
    text = result["text"]
    prompt_tokens = result["prompt_tokens"]
    completion_tokens = result["completion_tokens"]

    cost = estimate_cost(model, prompt_tokens, completion_tokens)

    if debug:
        print(f"\n{'┄' * 60}")
        print(
            f"  🐛 DEBUG — Response ({elapsed:.1f}s, {prompt_tokens}+{completion_tokens} tokens, ${cost:.4f} est.):"
        )
        print(f"{'┄' * 60}")
        print(text)
        print(f"{'┄' * 60}")

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
        "raw": text,
        "elapsed": round(elapsed, 1),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "cost": cost,
    }


# ── Rapport helpers ──────────────────────────────────────────────

RAPPORT_HEADER = """\
# Rapport d'extraction du corpus bilingue

> Généré automatiquement par `ocr_openai.py`
> Dernière mise à jour : {date}
> Livre : `{book_name}`
> Modèle : `{model}`

## Synthèse globale

{synthese}

## Rapport détaillé

| Image | Paires | Statut | Score | Temps | Coût | Remarques |
|-------|-------:|--------|------:|------:|-----:|----------|
"""


def load_rapport(rapport_path: Path) -> tuple[list[dict], list[str]]:
    """Charge les lignes du tableau existantes et les observations."""
    rows: list[dict] = []
    observations: list[str] = []
    if not rapport_path.exists():
        return rows, observations

    text = rapport_path.read_text(encoding="utf-8")

    # Parse table rows: Image | Paires | Statut | Score | Temps | Coût | Remarques
    for m in re.finditer(
        r"^\|\s*`?(\d+\.png)`?\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|",
        text,
        re.MULTILINE,
    ):
        rows.append(
            {
                "image": m.group(1).strip(),
                "pairs": m.group(2).strip(),
                "statut": m.group(3).strip(),
                "score": m.group(4).strip(),
                "time": m.group(5).strip(),
                "cost": m.group(6).strip(),
                "remarques": m.group(7).strip(),
            }
        )

    # Parse observations
    obs_match = re.search(
        r"## Suggestions d'amélioration du prompt\s*\n(.*)", text, re.DOTALL
    )
    if obs_match:
        for line in obs_match.group(1).strip().splitlines():
            line = line.strip()
            if line.startswith("- "):
                observations.append(line[2:])

    return rows, observations


def write_rapport(
    rapport_path: Path,
    rows: list[ReportRow],
    observations: list[str],
    model: str = DEFAULT_MODEL,
    total_pages: int | None = None,
    book_name: str = "",
) -> None:
    """Réécrit le rapport complet à partir des données."""
    stats = compute_summary_stats(rows)
    total = stats.total_pages
    avg_pairs = stats.total_pairs / total if total else 0
    avg_time = stats.total_time / total if total else 0
    avg_cost = stats.total_cost / total if total else 0

    pages_label = f"{total} / {total_pages}" if total_pages else str(total)
    synthese_lines = [
        f"- **Pages traitées** : {pages_label}",
        f"- **Paires extraites** : {stats.total_pairs} ({avg_pairs:.1f} /page)",
        f"- **OK** : {stats.n_ok} — **Difficultés** : {stats.n_diff} — **Impossible** : {stats.n_imp}"
        + (f" — **Erreurs** : {stats.n_err}" if stats.n_err else ""),
        f"- **Score** : moy {stats.avg_score:.0f}% · min {stats.min_score}% · max {stats.max_score}%",
        f"- **Temps** : {stats.total_time / 60:.1f} min ({avg_time:.1f}s /page)",
        f"- **Coût** : ${stats.total_cost:.4f} (${avg_cost:.4f} /page)",
    ]
    synthese = "\n".join(synthese_lines)

    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = RAPPORT_HEADER.format(
        date=date, synthese=synthese, model=model, book_name=book_name
    )

    for r in sorted(rows, key=image_sort_key):
        row_time = r.get("time", "")
        row_cost = r.get("cost", "")
        row_pairs = r.get("pairs", "0")
        out += f"| `{r['image']}` | {row_pairs} | {r['statut']} | {r['score']}% | {row_time} | {row_cost} | {r['remarques']} |\n"

    # Prompt improvement suggestions — group by GLOBAL vs BOOK
    unique_obs = list(dict.fromkeys(observations))  # deduplicate, preserve order
    if unique_obs:
        global_obs = [o for o in unique_obs if o.startswith("[GLOBAL]")]
        book_obs = [o for o in unique_obs if o.startswith("[BOOK]")]
        other_obs = [
            o
            for o in unique_obs
            if not o.startswith("[GLOBAL]") and not o.startswith("[BOOK]")
        ]

        out += "\n## Suggestions d'amélioration du prompt\n"

        if global_obs:
            out += "\n### Prompt global (`extract_bilingual_corpus.md`)\n\n"
            for obs in global_obs:
                out += f"- {obs}\n"

        if book_obs:
            out += "\n### Prompt spécifique au livre\n\n"
            for obs in book_obs:
                out += f"- {obs}\n"

        if other_obs:
            out += "\n### Autres observations\n\n"
            for obs in other_obs:
                out += f"- {obs}\n"

    rapport_path.write_text(out, encoding="utf-8")


# ── Main ─────────────────────────────────────────────────────────


def process_book_ocr(
    client: OpenAI,
    book_dir: Path,
    corpus_dir: Path,
    workflow: str,
    rapport_path: Path | None = None,
    model: str = DEFAULT_MODEL,
    debug: bool = False,
    limit: int | None = None,
) -> int:
    """Process all images in a single book directory.

    If rapport_path is None, the report summary is printed to stdout
    but not written to disk (useful for single-book test runs).
    If limit is set, only process a random sample of N pages.

    Returns the number of images processed.
    """
    images = sorted(book_dir.glob("*.png"))
    if not images:
        print(f"  ⚠️  No images found in {book_dir}/")
        return 0

    # Filter out dropped pages
    from scripts.utils import load_droplist, should_drop_page

    drop_pages = load_droplist(book_dir.name)
    if drop_pages:
        before = len(images)
        images = [img for img in images if not should_drop_page(img, drop_pages)]
        skipped = before - len(images)
        if skipped:
            print(f"  ⏭️  {skipped} pages in droplist, skipping")

    total_pages = len(images)
    corpus_dir.mkdir(parents=True, exist_ok=True)
    if rapport_path:
        rapport_path.parent.mkdir(parents=True, exist_ok=True)

    # Resume: skip if the .jsonl already exists (even if empty)
    to_process = [
        img for img in images if not (corpus_dir / f"{img.stem}.jsonl").exists()
    ]

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

    for i, img in enumerate(to_process, 1):
        print(f"\n  [{i}/{len(to_process)}] Traitement de {img.name}...")
        try:
            result = process_single_image(
                client, img, workflow, model=model, debug=debug
            )

            # Save JSONL
            jsonl_path = corpus_dir / f"{img.stem}.jsonl"
            n_pairs = write_jsonl(jsonl_path, result["jsonl"])
            cost_str = format_cost(result["cost"])
            print(
                f"     -> {jsonl_path.name} ({n_pairs} paires)  ⏱ {result['elapsed']}s  💰 {cost_str}"
            )

            # Add row to report table
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

            # Rewrite report after each image (for resumability)
            if rapport_path:
                write_rapport(
                    rapport_path,
                    rows,
                    observations,
                    model=model,
                    total_pages=total_pages,
                    book_name=book_dir.name,
                )

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
            (corpus_dir / f"{img.stem}.jsonl").touch()
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

    # --- Per-book summary ---
    stats = compute_summary_stats(rows)
    book_name = book_dir.name
    print(
        f"\n  📖 {book_name} — {stats.total_pages} pages · {stats.total_pairs} paires"
        f" · moy {stats.avg_score:.0f}% · ${stats.total_cost:.2f} · {stats.total_time / 60:.1f} min"
    )

    if rapport_path:
        print(f"     Rapport : {rapport_path.resolve()}")

    # Print prompt suggestions if any
    unique_obs = list(dict.fromkeys(observations))
    if unique_obs:
        print(f"\n  💡 Suggestions d'amélioration du prompt ({len(unique_obs)}) :")
        for obs in unique_obs[:10]:  # cap at 10 for stdout
            print(f"     {obs}")
        if len(unique_obs) > 10:
            print(f"     ... et {len(unique_obs) - 10} autres (voir rapport)")

    return len(to_process)


def main(argv=None):
    """Entry point. Pass argv list for programmatic use, or None for CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="OCR extraction of bilingual Breton-French corpus using OpenAI VLM.",
    )
    parser.add_argument(
        "--targets",
        nargs="*",
        help="Book subdirectory name(s) under pages/ or individual image file path(s). Default: all.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output path. For books: parent directory (JSONL goes to <dir>/<book>/). "
        "For a single image: directory or .jsonl file path. "
        "Default: corpus/<book>/<model>/",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Debug mode: print full prompts and LLM responses.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only N random pages per book (for testing).",
    )
    args = parser.parse_args(argv)

    provider = detect_provider(args.model)
    client = create_client(provider)
    pages_dir = PROJECT_ROOT / "pages"
    reports_root = PROJECT_ROOT / "reports"

    # Default corpus root: corpus/   (overridden by --output)
    corpus_root = args.output if args.output is not None else PROJECT_ROOT / "corpus"

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
    is_single_book = len(book_dirs) == 1 and not single_images
    is_single_image = len(single_images) == 1 and not book_dirs
    if is_single_book:
        print(f"📥 Entrée : {book_dirs[0].resolve()}/")
        print(
            f"📂 Sortie : {(corpus_root / book_dirs[0].name / args.model).resolve()}/"
        )
    elif is_single_image:
        print(f"📥 Entrée : {single_images[0].resolve()}")
        img_book = single_images[0].parent.name
        print(f"📂 Sortie : {(corpus_root / img_book / args.model).resolve()}/")
    else:
        print(f"📂 Sortie : {corpus_root.resolve()}/")

    total_processed = 0

    # Process full book directories
    for book_dir in book_dirs:
        book_name = book_dir.name
        print(f"\n{'─' * 60}")
        print(f"📖 {book_name}")
        print(f"{'─' * 60}")

        book_workflow = workflow + get_book_prompt(book_name)
        book_corpus_dir = corpus_root / book_name / args.model
        book_rapport_path = reports_root / book_name / args.model / "report.md"

        n = process_book_ocr(
            client,
            book_dir,
            book_corpus_dir,
            book_workflow,
            rapport_path=book_rapport_path,
            model=args.model,
            debug=args.debug,
            limit=args.limit,
        )
        total_processed += n

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
            if args.output is not None and args.output.suffix == ".jsonl":
                jsonl_path = args.output
                jsonl_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                img_corpus_dir = corpus_root / book_name / args.model
                img_corpus_dir.mkdir(parents=True, exist_ok=True)
                jsonl_path = img_corpus_dir / f"{img_path.stem}.jsonl"

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
    if is_single_book:
        book_name = book_dirs[0].name
        print(f"✅ Terminé. {total_processed} images traitées ({book_name}).")
        print(f"   Corpus : {(corpus_root / book_name / args.model).resolve()}/")
        print(f"   Rapports : {(reports_root / book_name / args.model).resolve()}/")
    elif book_dirs:
        print(f"✅ Terminé. {total_processed} images traitées.")
        print(f"   Corpus : {corpus_root.resolve()}/")
        print(f"   Rapports : {reports_root.resolve()}/")
    else:
        print(f"✅ Terminé. {total_processed} images traitées.")
    if single_images:
        for img_path in single_images:
            img_book = img_path.parent.name
            if args.output is not None and args.output.suffix == ".jsonl":
                print(f"   JSONL : {args.output.resolve()}")
            else:
                print(
                    f"   JSONL : {(corpus_root / img_book / args.model / f'{img_path.stem}.jsonl').resolve()}"
                )
    print(f"{'═' * 60}")


if __name__ == "__main__":
    main()
