---
description: Process a full book through the automated OCR pipeline
---

# OCR a full book

Run automated bilingual extraction on all pages of a given book using the `ocr_openai.py` script.

## Inputs

The user should provide:
- **Book name** — e.g. `bozec_methode_1933` (must match a folder in `pages/`)
- **Model** (optional) — e.g. `gpt-5.2-nano`, `gemini-2.5-flash`

If the book name is not provided, ask the user for it.

## CRITICAL RULE

always use **relative paths** to read write files not absolute paths

## Steps

1. **Verify the book directory exists**:
   - `list_dir` on `pages_enhanced/<book_name>` or check via `run_command`.

2. **Run the manual OCR workflow**:
   - For EACH .png file in `pages_enhanced/<book_name>/`:
     - Run the `ocr` workflow (`@[/ocr]`) with the target file: `pages_enhanced/<book_name>/<page_number>.png`.
     - DO NOT run all pages in parallel. Wait for one page to finish extracting, reviewing the results, and generating the JSONL before starting the next page.
     - After each page is done, **drop the page image from context** before moving on to the next page to avoid accumulating images in the context window.
     - **Before starting the next page**, re-read both `prompts/extract_bilingual_corpus.md` (global prompt) and `prompts/<book_name>.md` (book-specific prompt) using `view_file`. They may have been updated between pages.
   - *Note*: You can use the `list_dir` tool to get the list of files, and then loop through them.

3. **Monitor progress**:
   - After each page, give a quick update to the user.

4. **Generate global summary report**:
   - Read all per-page reports from `ocr/<book_name>/antigravity/<current_run>/reports/extraction/*.md` (exclude `report.md` itself)
   - Generate `ocr/<book_name>/antigravity/<current_run>/reports/extraction/report.md` with the following structure:
     ```markdown
     # OCR Report — <book_name>

     ## Statistiques globales

     | Métrique | Valeur |
     |---|---|
     | Pages traitées | <count> |
     | Paires extraites | <total> |
     | Score moyen | <average score> |
     | OK | <count> |
     | Difficultés | <count> |
     | Impossible | <count> |

     ## Commentaire général

     <Brief overall assessment of the book's OCR quality — 2-3 sentences>

     ## Suggestions d'amélioration du prompt

     ### [GLOBAL]
     - <deduplicated suggestion 1>
     - <deduplicated suggestion 2>

     ### [BOOK]
     - <deduplicated suggestion 1>
     - <deduplicated suggestion 2>
     ```
   - **Deduplication**: merge semantically equivalent observations from different pages into a single bullet. Do not repeat the same idea even if phrased differently across pages.
   - If no observations exist for a tag (`[GLOBAL]` or `[BOOK]`), write "Aucune" under that heading.
   - Use `write_to_file` with overwrite to create/update this file.
   - always use relative paths to read write files not absolute paths !!!