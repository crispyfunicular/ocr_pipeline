# AGENTS.md — OCR Pipeline

> Context file for AI coding assistants/agents

## Project Purpose

Extract bilingual Breton-French parallel corpora from scanned old books. The pipeline processes PDFs through several stages to produce structured JSONL output.

## Pipeline Architecture

```
PDFs (pdfs/)
  └── scripts/extract.py ──→ Raw PNGs (pages/<book>/)
        └── scripts/enhance.py ──→ Enhanced PNGs (pages_enhanced/<book>/)
              └── scripts/ocr.py ──→ JSONL (ocr/<book>/<model>/) + report.md
              └── scripts/ocr_batch.py ──→ (async) Gemini Batch API → same output
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
| `python pipeline.py review [book ...] [--model X]` | JSONL QA |
| `python pipeline.py corpus [book ...] [-o dir]` | Final corpus merge (stub) |

All scripts also work standalone: `python scripts/extract.py --help`

## Key Design Decisions

- **`main(argv=None)`** pattern: each script's `main()` accepts an optional argv list. When None, falls back to `sys.argv`. This allows both standalone and pipeline use.
- **Consistent positional `targets`**: all subcommands accept targets as positional args (PDFs for extract, book folder names or image paths for others).
- **Sanitized folder names** (`pdf_stem()`) are the thread between stages: the same name flows from `pages/` to `pages_enhanced/` to `ocr/<book>/<model>/`.
- **Important**: when calling `main(argv)`, always pass `[]` (empty list) for "no args" — never `None` (which means "use sys.argv").
- **`enhance_image()`** is the core enhancement function (CLAHE + optional DocRes). Accepts single images or batch via `process_book()`.
- **Default JPEG output**: Enhanced images are JPEG quality 85 by default (configurable via `--format` and `--jpeg-quality`). Use `--format png` for lossless output. JPEG provides ~5× disk savings over PNG with negligible OCR quality impact.
- **`discover_images()`**: Shared helper in `utils.py` that finds all images in a directory matching `IMAGE_EXTENSIONS`. Replaces hardcoded `*.png` globs across all pipeline stages.
- **`mime_type_for_image()`**: Shared helper in `utils.py` that maps file extensions to MIME types. Used by OCR API calls (OpenAI, Anthropic, Gemini) to send the correct `media_type` for both PNG and JPEG inputs.
- **Model subfolder**: OCR output is organized as `ocr/<book>/<model>/` (e.g. `ocr/my_book/gpt-5.2/`) so different models' outputs don't collide. Override with `-o`/`--output`.
- **Consistent `-o`/`--output`**: all stages accept `-o`/`--output` for overriding the output directory. For single-image OCR, `--output` can point to a `.jsonl` file path directly.
- **`--debug` mode**: prints full system/user prompts and raw LLM responses to stdout for troubleshooting.
- **Report metadata**: reports include per-image date, model, response time, and estimated cost (based on `MODEL_PRICING` dict). Synthèse shows total time and cost.
- **`parse_vlm_response()`**: shared response parser in `ocr.py` that extracts `=== JSONL ===` and `=== RAPPORT ===` blocks from raw VLM text. Used by both synchronous and batch OCR paths.
- **Batch folder**: each batch run creates `ocr/<book>/<model>/batch-YYYYMMDD-HHMM/` with `batch_state.json`, `prompt.md` (full prompt snapshot), `corpus/` (per-page JSONL), and `reports/` (quality report). State is kept after completion for auditability.
- **File API deduplication**: batch mode lists existing Gemini File API uploads by `display_name` (`ocr/<book>/<page>`) and skips re-uploading unchanged images. Uploads expire after 48h.
- **`scripts/utils.py`**: Shared module for DRY code: `ReportRow` TypedDict, `SummaryStats` dataclass, parsing helpers (`safe_int`, `safe_float`), formatting (`format_cost`), JSONL I/O (`write_jsonl`, `count_jsonl_pairs`), target discovery (`discover_targets`), and error detection (`is_auth_error`). Imported by `ocr.py`, `ocr_batch.py`, and `enhance.py`.

## Environment

- Python 3.11, venv in `.venv/`
- PyTorch 2.10.0+cu128 (RTX 5070 Ti, 16GB VRAM)
- DocRes (CVPR 2024) cloned in `docres/`, weights in `docres/checkpoints/docres.pkl`
- pip index override needed: `--index-url https://pypi.org/simple/`
- Run `./setup.sh` to set up everything from scratch (checks for `GEMINI_API_KEY`, `OPENAI_API_KEY`, and `ANTHROPIC_API_KEY`)

## Important Files

- `prompts/extract_bilingual_corpus.md` — System prompt for OpenAI extraction
- `prompts/<book_name>.md` — Optional per-book prompt overrides (appended to the base prompt when present)
- `scripts/utils.py` — Shared types (`ReportRow`, `SummaryStats`) and helpers used across stages
- `scripts/ocr.py` — Synchronous VLM-based OCR + `parse_vlm_response()` shared parser
- `scripts/ocr_batch.py` — Gemini Batch API: submit, poll, collect phases
- `reports/<book>/<model>/report.md` — Auto-generated extraction quality reports
- `requirements.txt` — Python dependencies (PyTorch installed separately)
- `setup.sh` — One-command environment setup (venv + deps + DocRes)
- `.gitignore` — Excludes venv, pages, enhanced pages, docres, logs
