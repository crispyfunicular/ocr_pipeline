# AGENTS.md — OCR Pipeline

> Context file for AI coding assistants/agents

## Project Purpose

Extract bilingual Breton-French parallel corpora from scanned old books. The pipeline processes PDFs through several stages to produce structured JSONL output.

## Pipeline Architecture

```
PDFs (pdfs/)
  └── scripts/extract_pages.py ──→ Raw PNGs (pages/<book>/)
        └── scripts/enhance_pages.py ──→ Enhanced PNGs (pages_enhanced/<book>/)
              └── scripts/ocr_openai.py ──→ JSONL (ocr/<book>/<model>/) + report.md
                    └── scripts/review_corpus.py ──→ Quality-assured JSONL
                          └── scripts/build_corpus.py ──→ Final corpus (stub)
```

## Entry Points

| Command | Description |
|---------|-------------|
| `python pipeline.py run [pdf ...]` | Full end-to-end pipeline |
| `python pipeline.py extract [pdf ...]` | PDFs → PNGs |
| `python pipeline.py enhance [book/image ...]` | Enhance (classical by default; use `--docres` / `--prepocr` for AI) |
| `python pipeline.py ocr [book ...] [--model X] [-o dir] [--debug]` | VLM-based OCR extraction |
| `python pipeline.py review [book ...] [--model X]` | JSONL QA |
| `python pipeline.py corpus [book ...] [-o dir]` | Final corpus merge (stub) |

All scripts also work standalone: `python scripts/extract_pages.py --help`

## Key Design Decisions

- **`main(argv=None)`** pattern: each script's `main()` accepts an optional argv list. When None, falls back to `sys.argv`. This allows both standalone and pipeline use.
- **Consistent positional `targets`**: all subcommands accept targets as positional args (PDFs for extract, book folder names or image paths for others).
- **Sanitized folder names** (`pdf_stem()`) are the thread between stages: the same name flows from `pages/` to `pages_enhanced/` to `ocr/<book>/<model>/`.
- **Important**: when calling `main(argv)`, always pass `[]` (empty list) for "no args" — never `None` (which means "use sys.argv").
- **`enhance_image()`** is the core enhancement function (CLAHE + optional DocRes). Accepts single images or batch via `process_book()`.
- **Model subfolder**: OCR output is organized as `ocr/<book>/<model>/` (e.g. `ocr/my_book/gpt-5.2/`) so different models' outputs don't collide. Override with `-o`/`--output`.
- **Consistent `-o`/`--output`**: all stages accept `-o`/`--output` for overriding the output directory. For single-image OCR, `--output` can point to a `.jsonl` file path directly.
- **`--debug` mode**: prints full system/user prompts and raw LLM responses to stdout for troubleshooting.
- **Report metadata**: reports include per-image date, model, response time, and estimated cost (based on `MODEL_PRICING` dict). Synthèse shows total time and cost.
- **`scripts/utils.py`**: Shared module for DRY code: `ReportRow` TypedDict, `SummaryStats` dataclass, parsing helpers (`safe_int`, `safe_float`), formatting (`format_cost`), JSONL I/O (`write_jsonl`, `count_jsonl_pairs`), target discovery (`discover_targets`), and error detection (`is_auth_error`). Imported by `ocr_openai.py` and `enhance_pages.py`.

## Environment

- Python 3.11, venv in `.venv/`
- PyTorch 2.10.0+cu128 (RTX 5070 Ti, 16GB VRAM)
- DocRes (CVPR 2024) cloned in `docres/`, weights in `docres/checkpoints/docres.pkl`
- pip index override needed: `--index-url https://pypi.org/simple/`
- Run `./setup.sh` to set up everything from scratch (checks for `OPENAI_API_KEY` in penultimate step)

## Important Files

- `prompts/extract_bilingual_corpus.md` — System prompt for OpenAI extraction
- `prompts/<book_name>.md` — Optional per-book prompt overrides (appended to the base prompt when present)
- `scripts/utils.py` — Shared types (`ReportRow`, `SummaryStats`) and helpers used across stages
- `reports/<book>/<model>/report.md` — Auto-generated extraction quality reports
- `requirements.txt` — Python dependencies (PyTorch installed separately)
- `setup.sh` — One-command environment setup (venv + deps + DocRes)
- `.gitignore` — Excludes venv, pages, enhanced pages, docres, logs
