# AGENTS.md — OCR Pipeline

> Quick-reference for AI coding assistants. For full system architecture, data flow, and stage details, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Project Purpose

Extract bilingual Breton-French parallel corpora from scanned old books. The pipeline processes PDFs through several stages to produce structured JSONL output.

## Pipeline Overview

```
PDFs (pdfs/)
  └── src/extract.py ──→ Raw PNGs (pages/<book>/)
        └── src/enhance.py ──→ Enhanced PNGs (pages_enhanced/<book>/)
              └── src/ocr/ ──→ ocr/<book>/<model[-think-level]>/<run>/extracted/*.jsonl
              │     ├── __init__.py  ← unified CLI (--batch flag routes to batch)
              │     ├── core.py      ← shared infra + run-folder management
              │     ├── providers.py  ← VLM clients, retry, API wrappers
              │     ├── reports.py   ← report template + helpers
              │     ├── sync.py      ← page-by-page VLM processing
              │     └── batch.py     ← Gemini Batch API (async, 50% cost)
              └── src/review.py ──→ Quality-assured JSONL
                    └── src/corpus.py ──→ Final corpus
```

## Entry Points

| Command | Description |
|---------|-------------|
| `python pipeline.py run [pdf ...]` | Full end-to-end pipeline |
| `python pipeline.py extract [pdf ...]` | PDFs → PNGs |
| `python pipeline.py enhance [book/image ...] [--format jpg|png] [--jpeg-quality N]` | Enhance (classical by default; use `--docres` / `--prepocr` for AI) |
| `python pipeline.py ocr [book ...] [--model X] [-o dir] [--debug]` | VLM-based OCR extraction (synchronous) |
| `python pipeline.py ocr [book ...] --batch [--model X] [--limit N]` | Submit OCR via Gemini Batch API (async, 50% cost) |
| `python pipeline.py ocr ... --book-prompt prompts/X-next.md` | Test a different book prompt version |
| `python pipeline.py ocr ... --main-prompt prompts/extract_bilingual_corpus-next.md` | Test a different main prompt version |
| `python pipeline.py ocr ... --thinking high` | Control Gemini thinking level (off/minimal/low/medium/high) |
| `python pipeline.py batch_status [book ...] [--wait] [--cancel]` | Check / collect Gemini Batch API results |
| `python pipeline.py review [book ...] --run <folder> [--model X]` | JSONL QA (requires explicit `--run`) |
| `python pipeline.py corpus [run_folder ...]` | Deduplicate extracted JSONL into `<run>/corpus/<book>.jsonl` |
| `/review-ocr-extraction <extraction_folder>` | LLM-as-Judge quality review (agent workflow) |

All scripts also work standalone: `python -m src.ocr --help`

## Conventions & Gotchas (Agent-Specific)

These are patterns and pitfalls that AI agents must follow when editing this codebase:

- **`main(argv=None)` pattern**: every pipeline module's `main()` accepts an optional argv list. When `None`, falls back to `sys.argv`. Always pass `[]` (empty list) for "no args" — never `None`.
- **One step = one module**: pipeline steps are either single `.py` files or packages (a directory with `__init__.py`).
- **Consistent positional `targets`**: all subcommands accept targets as positional args (PDFs for extract, book folder names or image paths for others).
- **Consistent `-o`/`--output`**: all stages accept `-o`/`--output` for overriding the output directory.
- **Sanitized folder names** (`pdf_stem()`) are the thread between stages: the same name flows from `pages/` to `pages_enhanced/` to `ocr/<book>/<model>/`.
- **`model_dir_name()`**: always use this helper when building model directory paths — it handles the `-think-<level>` suffix.
- **No empty JSONL on error**: API failures must not create empty `.jsonl` files. Only successful extractions produce output. This ensures failed pages are automatically retried on resume.
- **Typed return contracts**: `ParsedResponse` and `VLMResult` TypedDicts in `core.py` formalize return types — keep them in sync if changing function signatures.
- **`[] or None` bug pattern**: never write `argv or None` — use explicit `is None` checks. `[]` is falsy in Python.

## Environment

- Python 3.11, venv in `.venv/`
- PyTorch 2.10.0+cu128 (RTX 5070 Ti, 16GB VRAM)
- DocRes (CVPR 2024) cloned in `docres/`, weights in `docres/checkpoints/docres.pkl`
- pip index override needed: `--index-url https://pypi.org/simple/`
- Run `./setup.sh` to set up everything from scratch (checks for `GEMINI_API_KEY`, `OPENAI_API_KEY`, and `ANTHROPIC_API_KEY`)

## Important Files

- `prompts/extract_bilingual_corpus.md` — System prompt for VLM extraction
- `prompts/<book_name>.md` — Optional per-book prompt overrides (appended to the base prompt when present)
- `prompts/review/bilingual-ocr-extraction-review.md` — Global review prompt (LLM-as-Judge rubric, methodology, output format)
- `prompts/review/<book_name>-ocr-review.md` — Per-book review criteria (appended to global review prompt)
- `.agents/workflows/review-ocr-extraction.md` — Agent workflow orchestrating quality reviews
- `src/utils.py` — Shared types (`ReportRow`, `SummaryStats`) and helpers used across stages
- `src/ocr/` — OCR pipeline step (package)
  - `core.py` — Constants, TypedDicts, cost estimation, response parsing, run-folder management
  - `providers.py` — VLM client creation, retry logic, API call wrappers, `process_single_image()`
  - `reports.py` — Report template, `load_rapport()`, `write_rapport()`, `write_page_report()`
  - `sync.py` — Synchronous page-by-page OCR processing
  - `batch.py` — Gemini Batch API: submit, poll, collect
  - `__init__.py` — Unified `main()` entry point with `--batch` flag
  - `__main__.py` — Enables `python -m src.ocr`
- `tests/test_ocr_core.py` — Unit tests for OCR core pure functions (42 tests)
- `tests/test_extract.py` — Unit tests for PDF extraction: `pdf_stem`, `extract_pages`, droplist, CLI (9 tests)
- `tests/test_enhance.py` — Unit tests for enhance copy/compress: no-op copy, JPEG/PNG output, quality, droplist, pure helpers (17 tests)
- `ocr/<book>/<model>/<run>/reports/extraction/report.md` — Auto-generated extraction quality reports
- `ocr/<book>/<model>/<run>/reports/review/review.md` — LLM-as-Judge quality review reports
- `requirements.txt` — Python dependencies (PyTorch installed separately)
- `setup.sh` — One-command environment setup (venv + deps + DocRes)
- `.gitignore` — Excludes venv, pages, enhanced pages, docres, logs
