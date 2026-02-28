# 📜 Breton-French OCR Pipeline

A multi-stage pipeline for extracting bilingual **Breton-French** parallel corpora from scanned historical books (1860s–1940s). The extracted data produces JSONL files of aligned `{"breton": "...", "français": "..."}` pairs suitable for training translation models, building dictionaries, or linguistic research.

## Quick Start

```bash
# 1. Set up the environment (venv, dependencies, DocRes AI model)
./setup.sh

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Place your PDFs in pdfs/

# 4. Run the full pipeline
python pipeline.py run
```

---

## Pipeline Overview

```
PDFs → extract → PNGs → enhance → Enhanced PNGs → ocr → JSONL → cleanup → corpus
```

| Stage | Description | Script |
|-------|-------------|--------|
| **extract** | Render PDF pages as 300 DPI PNGs | `scripts/extract_pages.py` |
| **enhance** | CLAHE contrast + optional DocRes AI restoration | `scripts/enhance_pages.py` |
| **ocr** | VLM-based bilingual text extraction (OpenAI) | `scripts/ocr_openai.py` |
| **cleanup** | Quality assurance on extracted JSONL | `scripts/cleanup_corpus.py` *(stub)* |
| **corpus** | Merge per-page JSONL into final corpus | `scripts/build_corpus.py` *(stub)* |

### How the OCR stage works

The OCR stage sends each page image to an OpenAI Vision model along with a **two-layer prompt system**:

1. **Base prompt** (`prompts/extract_bilingual_corpus.md`) — defines the general extraction workflow, JSONL output format, quality rules, and exclusion criteria applicable to all books.
2. **Book-specific prompt** (`prompts/<book_name>.md`) — appended automatically based on the book folder name. Contains page layout descriptions, extraction rules, examples, and edge cases specific to that book.

The model returns structured JSONL pairs and a quality report (status, score, remarks) for each page.

---

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

## Usage

### Full pipeline

```bash
python pipeline.py run                              # All PDFs
python pipeline.py run pdfs/my_book.pdf              # One specific PDF
python pipeline.py run --no-docres                   # Without AI enhancement
```

### Individual stages

```bash
python pipeline.py extract                           # Extract all PDFs
python pipeline.py extract pdfs/my_book.pdf          # Extract one PDF
python pipeline.py enhance --no-docres               # Without DocRes AI
python pipeline.py enhance Manuel_1865               # Enhance one book
python pipeline.py enhance pages/Manuel_1865/05.png  # Enhance a single image
python pipeline.py ocr Manuel_1865                   # OCR one book
python pipeline.py ocr --model gpt-4.1-mini page.png # OCR a single page with a specific model
python pipeline.py ocr --debug page.png              # Show full prompts & LLM response
```

### Standalone scripts

Each script can also be run directly with full CLI options:

```bash
python scripts/extract_pages.py --dpi 400 pdfs/my_book.pdf
python scripts/enhance_pages.py --docres --docres-task deblurring --compare 20
python scripts/ocr_openai.py --targets Manuel_1865
```

---

## Prompt System

Each book has a dedicated prompt file in `prompts/` that teaches the LLM how to extract bilingual pairs from that specific book's layout and formatting:

| Prompt file | Key rules |
|-------------|-----------|
| `extract_bilingual_corpus.md` | **Base prompt** — JSONL format, quality rules, exclusion criteria, normalization |
| `toullec_lexique_1865.md` | 4-column layout, parallel preface, gender suffix stripping |
| `colloque_1890.md` | 4-column verb lists, conversational dialogues, synonym handling |
| `colloque_lourec_1884.md` | Profession-based sections, disambiguating parentheses |
| `normant_lexique_1902.md` | Breton→French direction, conjugation tables, cross-references |
| `geriadur_lexique_1927.md` | French→Breton direction, sub-entry expansion, abbreviation tables |
| `roparz_cours_elementaire_1930.md` | DIVIZ dialogues, mutation tables, RÉSUMÉ pages |
| `bozec_methode_1933.md` | Facing-page alignment, illustration captions, pronunciation cleanup |
| `yez_hon_tadou_1940.md` | GERIADUR word lists, word families, bilingual conjugation |
| `daniel_ker_vreiz_1944.md` | Vocabulary with pronunciation, LENNADENN/POELLADENNOU exclusions |

> **Adding a new book:** Create a new `prompts/<book_folder_name>.md` file following the same structure. The OCR stage will automatically pick it up based on the folder name.

---

## Cost Estimation (OCR Stage)

| Model | Avg cost/page | Avg time/page | Accuracy | Full run (570 pages) |
|-------|--------------|---------------|----------|----------------------|
| `gpt-4.1-mini` | ~$0.004 | ~16s | Good — occasional column misalignment and OCR typos | **~$2.30** / ~2.5h |
| `gpt-5.2` | ~$0.021 | ~10s | Better precision, correct alignment, cleaner OCR | **~$12** / ~1.5h |

> **Recommendation:** Use `gpt-5.2` (default) for production runs — the higher accuracy justifies the ~5× cost. Use `gpt-4.1-mini` for rapid iteration and prompt testing.

---

## Requirements

- **Python 3.11+**
- **NVIDIA GPU** with CUDA support (for DocRes enhancement stage; not required for OCR)
- **OpenAI API key** — set `OPENAI_API_KEY` env var for the OCR stage

### Setup

Run `./setup.sh` to automatically:
1. Create a Python virtual environment (`.venv`)
2. Install dependencies from `requirements.txt`
3. Install PyTorch with CUDA 12.8 support
4. Clone the [DocRes](https://github.com/ZZZHANG-jx/DocRes) repository and download model weights

---

## DocRes AI Enhancement

The pipeline integrates [DocRes](https://github.com/ZZZHANG-jx/DocRes) (CVPR 2024) for AI-powered document restoration. Available tasks:

| Task | Best for |
|------|----------|
| `appearance` | General cleanup, background normalization (default) |
| `deblurring` | Blurry or out-of-focus scans |
| `deshadowing` | Scans with shadows from book bindings |

```bash
python pipeline.py enhance --docres --docres-task appearance
```

---

## Project Structure

```
├── pipeline.py              # Unified CLI entry point
├── setup.sh                 # Environment setup script
├── requirements.txt         # Python dependencies
├── scripts/
│   ├── utils.py             # Shared helpers (types, parsing, target discovery)
│   ├── extract_pages.py     # PDF → PNG extraction
│   ├── enhance_pages.py     # Image enhancement (CLAHE + DocRes)
│   ├── ocr_openai.py        # OpenAI VLM-based OCR
│   ├── cleanup_corpus.py    # JSONL quality assurance (stub)
│   └── build_corpus.py      # Final corpus merge (stub)
├── prompts/
│   ├── extract_bilingual_corpus.md  # Base VLM extraction prompt
│   └── <book_name>.md              # Book-specific prompts (×9)
├── pdfs/                    # Source PDFs (not tracked)
├── pages/                   # Extracted page images (not tracked)
├── pages_enhanced/          # Enhanced images (not tracked)
├── corpus/                  # JSONL output: corpus/<book>/<model>/*.jsonl
└── reports/                 # Auto-generated quality reports
    └── <book>/<model>/report.md
```

## License

This pipeline is intended for personal/research use in corpus linguistics.
