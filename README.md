# 📜 Breton-French OCR Pipeline

> 🌐 **[Showcase site](https://crispyfunicular.github.io/ocr_pipeline/)** — interactive overview of the project, corpus, and metrics.

A multi-stage pipeline for extracting bilingual **Breton-French** parallel corpora from scanned historical books (1860s–1940s). Produces JSONL files of aligned `{"breton": "...", "français": "..."}` pairs suitable for training translation models, building dictionaries, or linguistic research.

## Corpus

The corpus spans **800+ pages** across **9 historical Breton-language books**:

| Book | Period | Type | Pages | Description |
|------|--------|------|-------|-------------|
| `toullec_lexique_1865` | 1865 | Lexicon | 87 | Bilingual French-Breton vocabulary by theme, with a parallel preface |
| `colloque_lourec_1884` | 1884 | Phrasebook | 72 | 4-column vocabulary lists by profession + conversational dialogues |
| `normant_lexique_1902` | 1902 | Dictionary | 71 | Breton→French dictionary with conjugation tables (KAOUT, BEZA) |
| `le_gonidec_vocabulaire_1919` | 1919 | Vocabulary | 313 | French-Breton vocabulary |
| `geriadur_lexique_1927` | 1927 | Medical lexicon | 22 | French→Breton anatomical/medical terminology with sub-entries |
| `roparz_cours_elementaire_1930` | 1930 | Course | 31 | Elementary Breton course with vocabulary, dialogues (DIVIZ), and exercises |
| `bozec_methode_1933` | 1933 | Method | 78 | Breton method with facing-page bilingual lessons and illustrations |
| `yez_hon_tadou_1940` | 1940 | Course | 96 | Breton course with GERIADUR word lists, word families, and conjugation |
| `daniel_ker_vreiz_1944` | 1944 | Course | 37 | Breton course with vocabulary, grammar examples, and verb tables |

### Droplist

Not every page contains bilingual content — covers, blank pages, tables of contents, appendices, and illustration-only pages have no translation pairs to extract. Each book can have a **droplist** (`droplist/<book>/drop_pages.json`) to exclude these pages from the OCR stage, **reducing API costs and processing time**.

```bash
python pipeline.py ignore pages_enhanced/my_book/05.png              # Ignore one page
python pipeline.py ignore pages_enhanced/my_book/01.png pages/my_book/02.png  # Multiple pages
python pipeline.py ignore pages/my_book/84.png                       # Works with pages/ too
```

Pages already in the droplist are skipped (idempotent). The JSON file is created automatically if it doesn't exist.

---

## Setup

### Requirements

- **Python 3.11+**
- **NVIDIA GPU** with CUDA support (for DocRes enhancement; not required for OCR)
- **API keys** — `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and/or `GEMINI_API_KEY` for the OCR stage

### Installation

**Base setup** (venv + core Python deps + API key check):

```bash
./setup.sh
source .venv/bin/activate
```

**With image enhancement tools** (PyTorch+CUDA, DocRes, ResShift — requires NVIDIA GPU):

```bash
./setup.sh --with-enhance
source .venv/bin/activate
```

---

## Pipeline Overview

```
pdfs/ → extract → pages/ → enhance → pages_enhanced/ → ocr → ocr/<book>/<model>/ → review → review/<book>/ → [human correction] → corpus → corpus/<book>.jsonl
```

| # | Stage | Input | Output | Script | Description |
|---|-------|-------|--------|--------|-------------|
| 1 | **extract** | `pdfs/` | `pages/<book>/` | `src/extract.py` | Render PDF pages as 300 DPI PNGs |
| 2 | **enhance** | `pages/<book>/` | `pages_enhanced/<book>/` | `src/enhance.py` | Copy pages (no-op by default) or apply opt-in enhancements |
| 3 | **ocr** | `pages_enhanced/<book>/` | `ocr/<book>/<model>/<run>/` | `src/ocr/` | VLM-based bilingual text extraction |
| 4 | **review** | `ocr/<book>/<model>/<run>/extracted/` | `review/<book>/` + `reports/<book>/` | `src/review.py` | Copy JSONL to review folder + quality assurance |
| 5 | **diff** | `ocr/`, `review/` | stdout | `src/diff.py` | Compare two JSONL directories/files to see human corrections |
| 6 | **evaluate** | `error_rates/<book>/` | stdout | `src/evaluate.py` | Compute WER & CER against human reference |
| 7 | **corpus** | `review/<book>/` | `corpus/<book>.jsonl` | `src/corpus.py` | Deduplicate and merge reviewed JSONL into one file per book |

## Pipeline Usage

```bash
# Full pipeline — all PDFs (classical enhancement only)
python pipeline.py run

# Full pipeline — one specific PDF
python pipeline.py run pdfs/my_book.pdf

# Full pipeline — with AI enhancement (requires --with-enhance setup)
python pipeline.py run --docres --prepocr

# Individual stages
python pipeline.py extract
python pipeline.py enhance
python pipeline.py ocr
```

---

## Extract

### Extract Overview

Renders each page of a PDF as a 300 DPI PNG image using PyMuPDF. Each PDF's pages are saved to `pages/<pdf_stem>/`.

### Extract Usage

```bash
python pipeline.py extract                           # All PDFs in pdfs/
python pipeline.py extract pdfs/my_book.pdf           # One specific PDF
python pipeline.py extract pdfs/a.pdf pdfs/b.pdf      # Multiple PDFs

# Direct script usage with extra options
python src/extract.py --dpi 400 pdfs/my_book.pdf
```

---

## Enhance

### Enhance Overview

By default, `enhance` is a **no-op**: pages are copied from `pages/` to `pages_enhanced/` without any processing. All enhancements are explicit opt-in flags. Three reasons:

- **GPU required** for AI models (DocRes, PreP-OCR) — not available in all environments
- **Heavy dependencies** — PyTorch, model weights (~1 GB) only installed with `./setup.sh --with-enhance`
- **Frontier VLMs work better on originals** — modern models like `gpt-5.2` handle degraded scans well enough that preprocessing can hurt more than it helps

> [!IMPORTANT]
> `--docres` and `--prepocr` require an NVIDIA GPU and heavy dependencies. Run `./setup.sh --with-enhance` before using them. `--classical` works with the base install.

Available flags (applied in this order):

| Flag | What it does | Requires |
|------|-------------|----------|
| `--classical` | Grayscale + CLAHE contrast equalization | Base install |
| `--docres` | DocRes AI: deshadowing → deblurring → appearance ([CVPR 2024](https://github.com/ZZZHANG-jx/DocRes)) | `--with-enhance` + GPU |
| `--prepocr` | PreP-OCR ResShift diffusion deblurring, 256×256 tiles ([PreP-OCR](https://github.com/NikoGuan/PreP-OCR)) | `--with-enhance` + GPU |
| `--denoise` | Bilateral denoising (smooths paper grain) | Base install |
| `--binarize` | Adaptive Gaussian binarization (B&W output) | Base install |
| `--upscale` | 2× Lanczos upscale | Base install |

### Enhance Usage

```bash
python pipeline.py enhance                                        # No-op: plain copy to pages_enhanced/
python pipeline.py enhance --classical                            # Grayscale + CLAHE
python pipeline.py enhance --docres                               # DocRes AI only (requires --with-enhance)
python pipeline.py enhance --docres --classical                   # DocRes + CLAHE
python pipeline.py enhance --prepocr --classical                  # PreP-OCR + CLAHE
python pipeline.py enhance --docres --prepocr --classical         # Full: DocRes + PreP-OCR + CLAHE
python pipeline.py enhance --docres --docres-tasks appearance     # Only one DocRes task
python pipeline.py enhance my_book                                # One book
python pipeline.py enhance pages/my_book/05.png                   # Single image

# Direct script usage
python src/enhance.py --classical --binarize --upscale
```

---

## Compare

### Compare Overview

Generates a comparison matrix of **all permutations** of the three enhancement stages (DocRes, PreP-OCR, Classical) for a single page. Useful for evaluating which ordering produces the best results for OCR.

Outputs **19 images** to `compare/<book>/<page>/`:
- `original.png` — unmodified input
- 3 individual DocRes sub-steps (`docres_deshadowing`, `docres_deblurring`, `docres_appearance`)
- 3 individual steps (`docres_pipeline`, `prepocr`, `classical`)
- 6 two-step permutations (e.g. `docres_pipeline-prepocr`, `classical-docres_pipeline`)
- 6 three-step permutations (e.g. `docres_pipeline-prepocr-classical`)

Two-step and three-step outputs reuse cached intermediate results to avoid redundant model passes.

### Compare Usage

```bash
python pipeline.py compare pages/my_book/17.png
```

## OCR

### OCR Overview

Sends each page image to a Vision Language Model (VLM) and parses structured bilingual output. Uses a **two-layer prompt system**:

1. **Base prompt** (`prompts/extract_bilingual_corpus.md`) — defines the general extraction workflow, JSONL output format, quality rules, and exclusion criteria.
2. **Book-specific prompt** (`prompts/<book_name>.md`) — appended automatically based on folder name. Contains page layout descriptions, extraction rules, examples, and edge cases.

The model returns structured JSONL pairs and a quality report (status, score, remarks) for each page. Processing is **resumable** — pages with existing `.jsonl` files are skipped.

**Supported providers:**

| Provider | Models | API key env var |
|----------|--------|-----------------|
| OpenAI | `gpt-5.2` (default), `gpt-4.1-mini`, `o3`, etc. | `OPENAI_API_KEY` |
| Anthropic | `claude-sonnet-4-6`, `claude-haiku-4.5`, `claude-opus-4`, etc. | `ANTHROPIC_API_KEY` |
| Google | `gemini-3.1-pro`, `gemini-3-flash`, `gemini-2.5-pro`, etc. | `GEMINI_API_KEY` |

### OCR Usage

```bash
python pipeline.py ocr                                  # All books, default model
python pipeline.py ocr my_book                          # One book
python pipeline.py ocr --model gpt-4.1-mini             # Cheaper OpenAI model
python pipeline.py ocr --model claude-sonnet-4-6        # Anthropic
python pipeline.py ocr --model gemini-3.1-pro           # Google Gemini
python pipeline.py ocr pages/my_book/05.png             # Single image
python pipeline.py ocr --debug pages/my_book/05.png     # Show full prompts & response
python pipeline.py ocr --limit 5 my_book                # Random sample of 5 pages
python pipeline.py ocr --book-prompt prompts/my_book-next.md my_book   # Test a new book prompt
python pipeline.py ocr --main-prompt prompts/extract_bilingual_corpus-next.md  # Test a new base prompt
python pipeline.py ocr --thinking high my_book              # Deep reasoning (Gemini only)
```

### Cost Estimation

| Model | Provider | Avg cost/page | Avg time/page | Accuracy | Full run (570 pages) |
|-------|----------|--------------|---------------|----------|----------------------|
| `gpt-4.1-mini` | OpenAI | ~$0.004 | ~16s | Good — occasional column misalignment and OCR typos | **~$2.30** / ~2.5h |
| `gemini-3.1-pro` | Google | ~$0.010 | — | Not yet benchmarked | **~$5.70** |
| `claude-sonnet-4-6` | Anthropic | ~$0.015 | — | Not yet benchmarked | **~$8.50** |
| `gpt-5.2` | OpenAI | ~$0.021 | ~10s | Better precision, correct alignment, cleaner OCR | **~$12** / ~1.5h |

> **Recommendation:** Use `gpt-5.2` (default) for production runs — the higher accuracy justifies the ~5× cost. Use `gpt-4.1-mini` for rapid iteration and prompt testing. Cost estimates for Gemini and Anthropic are based on token pricing and are not yet benchmarked on this corpus.

### Prompt System

Each book has a dedicated prompt file in `prompts/` that teaches the LLM how to extract bilingual pairs from that specific book's layout:

| Prompt file | Key rules |
|-------------|-----------|
| `extract_bilingual_corpus.md` | **Base prompt** — JSONL format, quality rules, exclusion criteria |
| `toullec_lexique_1865.md` | 4-column layout, parallel preface, gender suffix stripping |
| `colloque_1890.md` | 4-column verb lists, conversational dialogues |
| `colloque_lourec_1884.md` | Profession-based sections, disambiguating parentheses |
| `normant_lexique_1902.md` | Breton→French direction, conjugation tables, cross-references |
| `geriadur_lexique_1927.md` | French→Breton direction, sub-entry expansion, abbreviations |
| `roparz_cours_elementaire_1930.md` | DIVIZ dialogues, mutation tables, RÉSUMÉ pages |
| `bozec_methode_1933.md` | Facing-page alignment, illustration captions |
| `yez_hon_tadou_1940.md` | GERIADUR word lists, word families, bilingual conjugation |
| `daniel_ker_vreiz_1944.md` | Vocabulary with pronunciation, LENNADENN exclusions |

> **Adding a new book:** Create `prompts/<book_folder_name>.md` following the same structure. The OCR stage picks it up automatically based on folder name.

> **Testing prompt changes:** To iterate on a prompt without losing existing run data, copy it to a `-next.md` variant (e.g. `prompts/my_book-next.md`) and pass it via `--book-prompt` or `--main-prompt`. The prompt hash changes automatically, so a new run folder is created.

---



## Review

### Review Overview

Copies JSONL files from `ocr/<book>/<model>/<run>/extracted/` to `review/<book>/` (flat, no model subfolder), then scans them for common errors and quality issues. Requires `--run` to specify which run folder to copy from. If `review/<book>/` already exists, a confirmation prompt is shown before erasing its content.

After the review step, humans can inspect and correct the JSONL files in `review/<book>/` before building the final corpus.

Checks include: missing/extra keys, empty values, invalid characters, length imbalance (≥ 3×), single-character entries, extremely long entries (> 256 chars), digit-only entries, truncated entries, identical pairs.

Generates a Markdown report at `reports/<book>/review.md`.

### Review Usage

```bash
python pipeline.py review --run 0001-20260314-1624                    # All books, specific run
python pipeline.py review --run 0001-20260314-1624 my_book           # One book
python pipeline.py review --run 0001-20260314-1624 --model gpt-5.2   # Specific model
python pipeline.py review --yes --run 0001-20260314-1624             # Skip confirmation prompts
```

---

## Diff

### Diff Overview

Compares two directories (or files) of JSONL data and reports added, removed, and modified entries line-by-line. The primary use case is comparing the original `ocr/` output with the human-corrected `review/` folder to see what was changed during manual review.

By default, it compares the `ocr` and `review` directories at the project root.

### Diff Usage

```bash
python pipeline.py diff                                  # Default: compares ocr/ against review/
python pipeline.py diff ocr/my_book review/my_book       # Compare specific book directories
python pipeline.py diff -v                               # Verbose: show exactly which lines changed
python pipeline.py diff ocr/my_book/01.jsonl review/my_book/01.jsonl # Compare specific files
```

---

## Evaluate

### Evaluate Overview

Computes **Word Error Rate (WER)** and **Character Error Rate (CER)** for OCR outputs against manually corrected human references. Useful for benchmarking model and prompt improvements.

Each book to evaluate needs:
- `error_rates/<book>/human_reference/` — gold-standard JSONL files (manually corrected)
- `error_rates/<book>/jsonl/` — hypothesis JSONL files (OCR output to evaluate)

Metrics are computed separately for the Breton and French sides of each pair.

### Evaluate Usage

```bash
python pipeline.py evaluate                    # All books in error_rates/
python pipeline.py evaluate my_book            # One specific book
```

---

## Corpus

### Corpus Overview

Reads per-page JSONL from `review/<book>/` (after human correction), removes exact `{breton, français}` duplicate pairs, and writes a single `corpus/<book>.jsonl` per book. Empty files are skipped.

### Corpus Usage

```bash
python pipeline.py corpus                                    # All books
python pipeline.py corpus geriadur_lexique_1927              # One book
python pipeline.py corpus -o /tmp/my_corpus                  # Custom output directory
```

---

## Project Structure

```
├── pipeline.py              # Unified CLI entry point
├── setup.sh                 # Environment setup script
├── requirements.txt         # Core Python dependencies
├── requirements-enhance.txt # Enhancement deps (installed with --with-enhance)
├── src/
│   ├── utils.py             # Shared helpers (types, parsing, target discovery)
│   ├── extract.py           # PDF → PNG extraction
│   ├── enhance.py           # Image enhancement (DocRes + PreP-OCR + CLAHE)
│   ├── ocr/                 # VLM-based OCR (package)
│   │   ├── core.py          # Constants, types, cost estimation, run-folder management
│   │   ├── providers.py     # VLM client creation, retry logic, API wrappers
│   │   ├── reports.py       # Report generation and parsing
│   │   ├── sync.py          # Synchronous page-by-page processing
│   │   └── batch.py         # Gemini Batch API: submit, poll, collect
│   ├── review.py            # JSONL quality assurance
│   ├── evaluate.py          # WER/CER evaluation against human reference
│   └── corpus.py            # Deduplicate and merge into corpus/<book>.jsonl
├── prompts/
│   ├── extract_bilingual_corpus.md  # Base VLM extraction prompt
│   └── <book_name>.md              # Book-specific prompts (×9)
├── pdfs/                    # Source PDFs (not tracked)
│   └── <book>.pdf
├── pages/                   # Extracted page PNGs (not tracked)
│   └── <book>/
│       ├── 01.png
│       ├── 02.png
│       └── ...
├── pages_enhanced/          # Enhanced images (not tracked)
│   └── <book>/
│       ├── 01.png
│       ├── 02.png
│       └── ...
├── ocr/                     # Raw OCR output (per book, per model, per run)
│   └── <book>/
│       └── <model>/
│           └── <NNNN>-<YYYYMMDD>-<HHMM>/
│               ├── prompt.md
│               ├── run_state.json
│               ├── extracted/
│               │   ├── 01.jsonl
│               │   └── ...
│               └── reports/extraction/
├── review/                  # Staging area for human correction
│   └── <book>/
│       ├── 01.jsonl
│       ├── 02.jsonl
│       └── ...
├── corpus/                  # Final deduplicated corpus
│   ├── <book>.jsonl
│   └── ...
├── gold/                    # Gold-standard evaluation data
│   └── <book>/
│       ├── human_reference/ # Gold-standard JSONL (manually corrected)
│       ├── jsonl/           # Hypothesis JSONL (OCR output to evaluate)
│       └── report.md        # CER/WER + silence/bruit analysis
├── docs/                    # Showcase landing page (GitHub Pages)
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── hero_illustration.png
├── droplist/                # Per-book page exclusion lists
│   └── <book>/
│       └── drop_pages.json  # JSON array of page numbers to skip
└── reports/                 # Auto-generated quality reports
    └── <book>/
        └── <model>/
            └── review.md
```

## License

This pipeline is intended for personal/research use in corpus linguistics.
