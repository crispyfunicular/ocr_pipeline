---
description: Run a quality review on an OCR extraction folder using LLM-as-Judge methodology
---

// turbo-all

# Review OCR Extraction Quality

## Usage

```
/review-ocr-extraction <extraction_folder>
```

Example:
```
/review-ocr-extraction ocr/bozec_methode_1933/gemini-3.1-pro-preview/0002-20260314-1759
```

## Prerequisites

The extraction folder must exist and contain:
- `extracted/*.jsonl` — extracted bilingual pairs
- `reports/extraction/report.md` — auto-generated extraction report

## Workflow

### 1. Resolve context

From the extraction folder path, derive:
- **Book name**: second path component (e.g., `bozec_methode_1933`)
- **Model**: third component (e.g., `gemini-3.1-pro-preview`)
- **Run ID**: fourth component (e.g., `0002-20260314-1759`)
- **Image folder**: `pages_enhanced/<book>/`
- **Book extraction prompt**: `prompts/<book>.md` (may not exist for all books)
- **Book review prompt**: `prompts/review/<book>-ocr-review.md` (may not exist yet)

Verify all required paths exist. If `pages_enhanced/<book>/` doesn't exist, abort.

### 2. Read the review prompts

Read the following files carefully — they define what to check and how to evaluate:
- `prompts/review/bilingual-ocr-extraction-review.md` (global review criteria)
- `prompts/review/<book>-ocr-review.md` (book-specific review criteria, if exists)
- `prompts/<book>.md` (book extraction prompt — needed to check rule compliance)
- `prompts/extract_bilingual_corpus.md` (global extraction prompt — for context)

### 3. Compute corpus-wide stats

Run these analyses across ALL JSONL files in `extracted/`:

```python
# Compute using inline Python commands:
# 1. Total pairs (raw line count)
# 2. Unique pairs (deduplicated on both fields)
# 3. Cross-page duplicates (pairs appearing in >1 file)
# 4. Malformed JSON lines (unparseable or missing required keys)
# 5. Short entries (breton field ≤ 2 characters) — list them
# 6. Abbreviation residuals (french field containing ' m.', ' f.', 'adj.', 'subst.', etc.)
# 7. Unresolved em-dashes (french field containing '—')
# 8. Pair count per page (min, max, avg, stddev)
```

Also check the extraction report for:
- Pages with status "Impossible" — cross-reference with images to detect false Impossibles
- Pages with 0 pairs that have corresponding images

### 4. Select pages for deep review

Select **5 pages** for image-based deep review using this strategy:
- 1 page with the **lowest** pair count (excluding legitimate 0s like title pages)
- 1 page with the **highest** pair count
- 1 page with **known issues** (from stats: malformed JSON, abbreviation residuals, etc.) — if none, pick a random page
- 2 **random** pages from the remaining pool

If any pages were flagged as "Impossible" with existing images, add them to the review set.

### 5. Deep review of selected pages

For each selected page, perform the review following the methodology in `bilingual-ocr-extraction-review.md`:

1. **View the page image** from `pages_enhanced/<book>/<page>.jpg` (or `.png`)
2. **Read the JSONL** from `extracted/<page>.jsonl`
3. **Phase 1**: Independently note what you'd extract from the image
4. **Phase 2**: Compare against the JSONL — identify correct, missing, incorrect, and deformed pairs
5. **Phase 3**: Check book-specific rules from the review prompt
6. Score each dimension using the rubric

### 6. Write the review report

Create the output at: `<extraction_folder>/reports/review/review.md`

Use this structure:

```markdown
# Quality Review — <book_name>

> **Run**: `<run_id>`
> **Model**: `<model>`
> **Reviewer**: Antigravity (LLM-as-Judge)
> **Date**: <today>
> **Pages reviewed**: N / total (strategy: lowest + highest + flagged + random)
> **Corpus**: X pairs (Y unique) across Z JSONL files

## Corpus Stats

| Metric | Value |
|--------|-------|
| Total pairs (raw) | |
| Unique pairs | |
| Cross-page duplicates | |
| Malformed JSON lines | |
| Short entries (≤2 chars) | |
| Abbreviation residuals | |
| Unresolved em-dashes | |
| False Impossible pages | |

## Page Verdicts

| Page | Pairs | Accuracy | Completeness | Issues |
|------|-------|----------|--------------|--------|
| pXX | NN | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | — |

## Issues

### 🔴 Critical
[or "None"]

### 🟡 Warning
[or "None"]

### 🟢 Info
[observations]

## Tricky Page Deep Reviews

[Per-page review details following the output format
from bilingual-ocr-extraction-review.md]

## Prompt Assessment

[Observations on the extraction prompt + book prompt — any rules missing or needing refinement?]

## Final Verdict

| Category | Rating |
|----------|--------|
| Accuracy | ⭐⭐⭐⭐⭐ |
| Completeness | ⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Prompt compliance | ⭐⭐⭐⭐⭐ |
| Data integrity | ⭐⭐⭐⭐⭐ |
| **Overall** | **⭐⭐⭐⭐½** |

### Required Actions
1. [numbered list, or "None — production-ready"]
```

### 7. Summary

After writing the report, provide a brief summary to the user:
- Overall verdict (star rating)
- Number of critical/warning/info issues
- Any required actions
