"""
OCR extraction report generation and parsing.

Handles reading, writing, and updating the per-book extraction reports
(markdown tables with per-page metrics) and per-page individual reports.
"""

import re
from datetime import datetime
from pathlib import Path

from scripts.ocr.core import DEFAULT_MODEL
from scripts.utils import (
    ReportRow,
    compute_summary_stats,
    format_cost,
    image_sort_key,
)

# ── Report template ──────────────────────────────────────────────

RAPPORT_HEADER = """\
# Rapport d'extraction du corpus bilingue

> Généré automatiquement par `scripts/ocr`
> Dernière mise à jour : {date}
> Livre : `{book_name}`
> Modèle : `{model}`

## Synthèse globale

{synthese}

## Rapport détaillé

| Image | Paires | Statut | Score | Temps | Coût | Remarques |
|-------|-------:|--------|------:|------:|-----:|----------|
"""


def load_rapport(rapport_path: Path) -> tuple[list[ReportRow], list[str]]:
    """Charge les lignes du tableau existantes et les observations."""
    rows: list[ReportRow] = []
    observations: list[str] = []
    if not rapport_path or not rapport_path.exists():
        return rows, observations

    text = rapport_path.read_text(encoding="utf-8")

    # Parse table rows: Image | Paires | Statut | Score | Temps | Coût | Remarques
    for m in re.finditer(
        r"^\|\s*`?(\d+\.\w+)`?\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|",
        text,
        re.MULTILINE,
    ):
        rows.append(
            ReportRow(
                image=m.group(1).strip(),
                pairs=m.group(2).strip(),
                statut=m.group(3).strip(),
                score=m.group(4).strip(),
                time=m.group(5).strip(),
                cost=m.group(6).strip(),
                remarques=m.group(7).strip(),
            )
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


def write_page_report(reports_dir: Path, img_name: str, result: dict) -> None:
    """Write a per-page extraction report to reports/extraction/XX.md."""
    stem = Path(img_name).stem
    report_path = reports_dir / f"{stem}.md"
    content = f"# Page {stem}\n\n"
    content += f"- **Statut**: {result['statut']}\n"
    content += f"- **Score**: {result['score']}\n"
    content += f"- **Temps**: {result.get('elapsed', 'N/A')}s\n"
    content += f"- **Coût**: {format_cost(result.get('cost'))}\n"
    content += f"- **Remarques**: {result.get('remarques', '')}\n"
    if result.get("observations") and result["observations"].lower() != "aucune":
        content += f"- **Observations workflow**: {result['observations']}\n"
    report_path.write_text(content, encoding="utf-8")
