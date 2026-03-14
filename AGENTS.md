# AGENTS.md — OCR Pipeline

> Context file for AI coding assistants/agents

## Project Purpose

Extract bilingual Breton-French parallel corpora from scanned old books. The pipeline processes PDFs through several stages to produce structured JSONL output.

## Pipeline Architecture

```
PDFs (pdfs/)
  └── scripts/extract.py ──→ Raw PNGs (pages/<book>/)
        └── scripts/enhance.py ──→ Enhanced PNGs (pages_enhanced/<book>/)
              └── scripts/ocr/ ──→ ocr/<book>/<model>/<run>/extracted/*.jsonl
              │     ├── __init__.py  ← unified CLI (--batch flag routes to batch)
              │     ├── core.py      ← shared infra + run-folder management
              │     ├── sync.py      ← page-by-page VLM processing
              │     └── batch.py     ← Gemini Batch API (async, 50% cost)
              └── scripts/review.py ──→ Quality-assured JSONL
                    └── scripts/corpus.py ──→ Final corpus
```

## Entry Points

| Command | Description |
|---------|-------------|
| `python pipeline.py run [pdf ...]` | Full end-to-end pipeline |
| `python pipeline.py extract [pdf ...]` | PDFs → PNGs |
| `python pipeline.py enhance [book/image ...] [--format jpg|png] [--jpeg-quality N]` | Enhance (classical by default; use `--docres` / `--prepocr` for AI) |
| `python pipeline.py ocr [book ...] [--model X] [-o dir] [--debug]` | VLM-based OCR extraction (synchronous) |
| `python pipeline.py ocr [book ...] --batch [--model X] [--limit N]` | Submit OCR via Gemini Batch API (async, 50% cost) |
| `python pipeline.py batch_status [book ...] [--wait] [--cancel]` | Check / collect Gemini Batch API results |
| `python pipeline.py review [book ...] --run <folder> [--model X]` | JSONL QA (requires explicit `--run`) |
| `python pipeline.py corpus [book ...] [-o dir]` | Final corpus merge (stub) |

All scripts also work standalone: `python -m scripts.ocr --help`

## Key Design Decisions

- **`main(argv=None)`** pattern: each script's `main()` accepts an optional argv list. When None, falls back to `sys.argv`. This allows both standalone and pipeline use.
- **One step = one module**: pipeline steps are either single `.py` files or packages (a directory with `__init__.py`). The OCR step is `scripts/ocr/` because it's large enough to warrant a package split.
- **Consistent positional `targets`**: all subcommands accept targets as positional args (PDFs for extract, book folder names or image paths for others).
- **Sanitized folder names** (`pdf_stem()`) are the thread between stages: the same name flows from `pages/` to `pages_enhanced/` to `ocr/<book>/<model>/`.
- **Important**: when calling `main(argv)`, always pass `[]` (empty list) for "no args" — never `None` (which means "use sys.argv").
- **`enhance_image()`** is the core enhancement function (CLAHE + optional DocRes). Accepts single images or batch via `process_book()`.
- **Default JPEG output**: Enhanced images are JPEG quality 85 by default (configurable via `--format` and `--jpeg-quality`). Use `--format png` for lossless output. JPEG provides ~5× disk savings over PNG with negligible OCR quality impact.
- **`discover_images()`**: Shared helper in `utils.py` that finds all images in a directory matching `IMAGE_EXTENSIONS`. Replaces hardcoded `*.png` globs across all pipeline stages.
- **`mime_type_for_image()`**: Shared helper in `utils.py` that maps file extensions to MIME types. Used by OCR API calls (OpenAI, Anthropic, Gemini) to send the correct `media_type` for both PNG and JPEG inputs.
- **Unified run-folder structure**: Both sync and batch OCR output to `ocr/<book>/<model>/<NNNN>-<YYYYMMDD>-<HHMM>/` containing `prompt.md`, `run_state.json`, `extracted/*.jsonl`, and `reports/extraction/`. The `<NNNN>` counter is 4-digit zero-padded and auto-incrementing.
- **Prompt-hash reuse**: `scripts/ocr/core.py` computes a SHA-256 hash (first 8 hex) of the full prompt (system + global + book). If the hash matches an existing non-completed run folder, that folder is reused for resuming. A hash change triggers a new run folder.
- **`run_state.json`**: Tracks run metadata (prompt hash, model, book, mode, status, processed pages, batch job info).
- **Per-page reports**: Each page gets an individual extraction report at `reports/extraction/XX.md` alongside the summary `reports/extraction/report.md`.
- **Consistent `-o`/`--output`**: all stages accept `-o`/`--output` for overriding the output directory. When passed, bypasses the run-folder structure entirely.
- **`--debug` mode**: prints full system/user prompts and raw LLM responses to stdout for troubleshooting.
- **Report metadata**: reports include per-image date, model, response time, and estimated cost (based on `MODEL_PRICING` dict). Synthèse shows total time and cost.
- **`parse_vlm_response()`**: shared response parser in `scripts/ocr/core.py` that extracts `=== JSONL ===` and `=== RAPPORT ===` blocks from raw VLM text. Used by both synchronous and batch OCR paths.
- **File API deduplication**: batch mode lists existing Gemini File API uploads by `display_name` (`ocr/<book>/<page>`) and skips re-uploading unchanged images. Uploads expire after 48h.
- **Retry with backoff**: `_retry_api_call()` in `core.py` wraps all VLM API calls with exponential backoff + jitter. Retries on 429 (rate limit), 5xx (server errors), and connection issues. Max 3 retries.
- **Typed return contracts**: `ParsedResponse` and `VLMResult` TypedDicts in `core.py` formalize the return types of `parse_vlm_response()` and `process_single_image()`.
- **`MAX_COMPLETION_TOKENS`**: module-level constant (4000) used by all three API callers. Centralizes token budget.
- **`--seed`**: optional CLI flag for reproducible `--limit` random sampling across sync and batch modes.
- **`scripts/utils.py`**: Shared module for DRY code: `ReportRow` TypedDict, `SummaryStats` dataclass, parsing helpers (`safe_int`, `safe_float`), formatting (`format_cost`), JSONL I/O (`write_jsonl`, `count_jsonl_pairs`), target discovery (`discover_targets`), and error detection (`is_auth_error`). Imported by `scripts/ocr/` and `scripts/enhance.py`.

## Environment

- Python 3.11, venv in `.venv/`
- PyTorch 2.10.0+cu128 (RTX 5070 Ti, 16GB VRAM)
- DocRes (CVPR 2024) cloned in `docres/`, weights in `docres/checkpoints/docres.pkl`
- pip index override needed: `--index-url https://pypi.org/simple/`
- Run `./setup.sh` to set up everything from scratch (checks for `GEMINI_API_KEY`, `OPENAI_API_KEY`, and `ANTHROPIC_API_KEY`)

## Important Files

- `prompts/extract_bilingual_corpus.md` — System prompt for VLM extraction
- `prompts/<book_name>.md` — Optional per-book prompt overrides (appended to the base prompt when present)
- `scripts/utils.py` — Shared types (`ReportRow`, `SummaryStats`) and helpers used across stages
- `scripts/ocr/` — OCR pipeline step (package)
  - `core.py` — Constants, TypedDicts, cost estimation, response parsing, run-folder management
  - `providers.py` — VLM client creation, retry logic, API call wrappers, `process_single_image()`
  - `reports.py` — Report template, `load_rapport()`, `write_rapport()`, `write_page_report()`
  - `sync.py` — Synchronous page-by-page OCR processing
  - `batch.py` — Gemini Batch API: submit, poll, collect
  - `__init__.py` — Unified `main()` entry point with `--batch` flag
  - `__main__.py` — Enables `python -m scripts.ocr`
- `tests/test_ocr_core.py` — Unit tests for OCR core pure functions (33 tests)
- `tests/test_extract.py` — Unit tests for PDF extraction: `pdf_stem`, `extract_pages`, droplist, CLI (9 tests)
- `tests/test_enhance.py` — Unit tests for enhance copy/compress: no-op copy, JPEG/PNG output, quality, droplist, pure helpers (17 tests)
- `ocr/<book>/<model>/<run>/reports/extraction/report.md` — Auto-generated extraction quality reports
- `requirements.txt` — Python dependencies (PyTorch installed separately)
- `setup.sh` — One-command environment setup (venv + deps + DocRes)
- `.gitignore` — Excludes venv, pages, enhanced pages, docres, logs
