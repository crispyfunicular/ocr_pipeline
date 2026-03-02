# 📜 Breton-French OCR Pipeline

A multi-stage pipeline for extracting bilingual **Breton-French** parallel corpora from scanned historical books (1860s–1940s). Produces JSONL files of aligned `{"breton": "...", "français": "..."}` pairs suitable for training translation models, building dictionaries, or linguistic research.

## Corpus

The corpus spans **570 pages** across **9 historical Breton-language books**:

| Book | Period | Type | Pages | Description |
|------|--------|------|-------|-------------|
| `toullec_lexique_1865` | 1865 | Lexicon | 87 | Bilingual French-Breton vocabulary by theme, with a parallel preface |
| `colloque_lourec_1884` | 1884 | Phrasebook | 74 | 4-column vocabulary lists by profession + conversational dialogues |
| `colloque_1890` | 1890 | Phrasebook | 74 | Similar to 1884 edition, 4-column verb lists and dialogues |
| `normant_lexique_1902` | 1902 | Dictionary | 71 | Breton→French dictionary with conjugation tables (KAOUT, BEZA) |
| `geriadur_lexique_1927` | 1927 | Medical lexicon | 22 | French→Breton anatomical/medical terminology with sub-entries |
| `roparz_cours_elementaire_1930` | 1930 | Course | 31 | Elementary Breton course with vocabulary, dialogues (DIVIZ), and exercises |
| `bozec_methode_1933` | 1933 | Method | 78 | Breton method with facing-page bilingual lessons and illustrations |
| `yez_hon_tadou_1940` | 1940 | Course | 96 | Breton course with GERIADUR word lists, word families, and conjugation |
| `daniel_ker_vreiz_1944` | 1944 | Course | 37 | Breton course with vocabulary, grammar examples, and verb tables |

---

## Setup

### Requirements

- **Python 3.11+**
- **NVIDIA GPU** with CUDA support (for DocRes enhancement; not required for OCR)
- **API keys** — `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY` for the OCR stage

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
PDFs → extract → PNGs → enhance → Enhanced PNGs → ocr → JSONL → review → corpus
```

| Stage | Description | Script |
|-------|-------------|--------|
| **extract** | Render PDF pages as 300 DPI PNGs | `scripts/extract_pages.py` |
| **enhance** | CLAHE contrast + optional DocRes AI + PreP-OCR deblurring | `scripts/enhance_pages.py` |
| **ocr** | VLM-based bilingual text extraction | `scripts/ocr_openai.py` |
| **review** | Quality assurance on extracted JSONL | `scripts/review_corpus.py` |
| **corpus** | Merge per-page JSONL into final corpus | `scripts/build_corpus.py` *(stub)* |

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
python scripts/extract_pages.py --dpi 400 pdfs/my_book.pdf
```

---

## Enhance

### Enhance Overview

Applies image enhancement to improve OCR accuracy on degraded historical scans. The default pipeline chains three stages:

1. **DocRes AI restoration** ([CVPR 2024](https://github.com/ZZZHANG-jx/DocRes)) — a Restormer model with Dynamic Task-Specific Prompts that runs **three tasks sequentially** by default:

   | Task | Order | Purpose |
   |------|-------|---------|
   | `deshadowing` | 1st | Remove shadows from book bindings and uneven lighting |
   | `deblurring` | 2nd | Sharpen blurry or out-of-focus text |
   | `appearance` | 3rd | Final background cleanup and contrast normalization |

2. **PreP-OCR deblurring** ([PreP-OCR](https://github.com/NikoGuan/PreP-OCR)) — a ResShift diffusion model trained specifically for historical document deblurring. Processes images in 256×256 tiles with 4-step diffusion sampling. **Off by default — enable with `--prepocr`.**

3. **Classical enhancement** — grayscale conversion + CLAHE contrast equalization, with optional bilateral denoising and adaptive binarization. **On by default.**

### Enhance Usage

```bash
python pipeline.py enhance                                        # Classical only (grayscale + CLAHE)
python pipeline.py enhance --docres                                # DocRes AI + classical
python pipeline.py enhance --prepocr                               # PreP-OCR + classical
python pipeline.py enhance --docres --prepocr                      # Full: DocRes + PreP-OCR + classical
python pipeline.py enhance --no-classical                          # No enhancement (passthrough)
python pipeline.py enhance --docres --docres-tasks appearance      # Only one DocRes task
python pipeline.py enhance --docres --docres-tasks deshadowing deblurring  # Pick specific DocRes tasks
python pipeline.py enhance my_book                                 # Enhance one book
python pipeline.py enhance pages/my_book/05.png                    # Enhance a single image

# Direct script usage with all options
python scripts/enhance_pages.py --binarize --upscale --compare 20
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
| Anthropic | `claude-sonnet-4`, `claude-haiku-4.5`, etc. | `ANTHROPIC_API_KEY` |

### OCR Usage

```bash
python pipeline.py ocr                                # All books, default model
python pipeline.py ocr my_book                        # One book
python pipeline.py ocr --model gpt-4.1-mini           # Cheaper model
python pipeline.py ocr --model claude-sonnet-4         # Anthropic
python pipeline.py ocr pages/my_book/05.png            # Single image
python pipeline.py ocr --debug pages/my_book/05.png    # Show full prompts & response
python pipeline.py ocr --limit 5 my_book               # Random sample of 5 pages
```

### Cost Estimation

| Model | Avg cost/page | Avg time/page | Accuracy | Full run (570 pages) |
|-------|--------------|---------------|----------|----------------------|
| `gpt-4.1-mini` | ~$0.004 | ~16s | Good — occasional column misalignment and OCR typos | **~$2.30** / ~2.5h |
| `gpt-5.2` | ~$0.021 | ~10s | Better precision, correct alignment, cleaner OCR | **~$12** / ~1.5h |

> **Recommendation:** Use `gpt-5.2` (default) for production runs — the higher accuracy justifies the ~5× cost. Use `gpt-4.1-mini` for rapid iteration and prompt testing.

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

---

## Droplist

### Droplist Overview

Some pages (covers, blank pages, appendices…) should be excluded from OCR processing. Each book can have a **droplist** — a JSON array of page numbers stored in `droplist/<book>/drop_pages.json`.

### Droplist Usage

```bash
python pipeline.py ignore pages_enhanced/my_book/05.png              # Ignore one page
python pipeline.py ignore pages_enhanced/my_book/01.png pages_enhanced/my_book/02.png  # Ignore multiple pages
python pipeline.py ignore pages/my_book/84.png                       # Also works with pages/
```

Pages already in the droplist are skipped (idempotent). The JSON file is created automatically if it doesn't exist.

---

## Review

### Review Overview

Quality assurance pass on extracted JSONL files.

---

## Corpus *(stub)*

### Corpus Overview

Merges per-page JSONL files into a final consolidated corpus. Not yet implemented.

---

## Project Structure

```
├── pipeline.py              # Unified CLI entry point
├── setup.sh                 # Environment setup script
├── requirements.txt         # Core Python dependencies
├── requirements-enhance.txt # Enhancement deps (installed with --with-enhance)
├── scripts/
│   ├── utils.py             # Shared helpers (types, parsing, target discovery)
│   ├── extract_pages.py     # PDF → PNG extraction
│   ├── enhance_pages.py     # Image enhancement (DocRes + CLAHE)
│   ├── ocr_openai.py        # VLM-based OCR (OpenAI / Anthropic)
│   ├── review_corpus.py     # JSONL quality assurance
│   └── build_corpus.py      # Final corpus merge (stub)
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
├── corpus/                  # Extracted JSONL pairs
│   └── <book>/
│       └── <model>/
│           ├── 01.jsonl
│           ├── 02.jsonl
│           └── ...
├── droplist/                # Per-book page exclusion lists
│   └── <book>/
│       └── drop_pages.json  # JSON array of page numbers to skip
└── reports/                 # Auto-generated quality reports
    └── <book>/
        └── <model>/
            └── report.md
```

## License

This pipeline is intended for personal/research use in corpus linguistics.
