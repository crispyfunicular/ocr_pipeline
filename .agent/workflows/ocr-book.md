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

4. **Review the results**:
   - Provide a final summary table to the user with the number of pairs extracted per page.