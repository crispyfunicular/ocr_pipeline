---
description: Run OCR on a single page using global+book prompts and store result for comparison
---

# OCR a single page

Run bilingual extraction on a single page image, applying both the global and book-specific prompts, and save the result as JSONL.

## Inputs

The user should provide:
- **Image path** — e.g. `pages_enhanced/bozec_methode_1933/25.png`

If not provided, ask the user for the image path.

## Steps

1. **Parse inputs** from the image path:
   - `book_name` = parent directory name (e.g. `bozec_methode_1933`)
   - `page_number` = filename stem (e.g. `25`)
   - Project root = `/home/cam/git/modyco/breton/ocr_pipeline`

2. **Read the global prompt**:
   - `view_file` on `<project_root>/prompts/extract_bilingual_corpus.md`

3. **Read the book-specific prompt** (if it exists):
   - `view_file` on `<project_root>/prompts/<book_name>.md`

4. **View the page image**:
   - `view_file` on the image path (binary/image viewing)

5. **Perform OCR extraction**:
   - Apply ALL rules from both prompts (global first, then book-specific overrides)
   - Extract bilingual pairs from the image
   - Follow the exact output format specified in the global prompt:
     ```
     === JSONL ===
     (one JSON line per pair)
     === /JSONL ===

     === RAPPORT ===
     Statut: OK | Difficultés | Impossible
     Score: <0-100>
     Remarques: <observations>
     Observations workflow: <suggestions or "aucune">
     === /RAPPORT ===
     ```

6. **Save the JSONL output**:
   - Create directory `<project_root>/corpus/<book_name>/antigravity/` if needed
   - Write ONLY the JSONL lines (not the report) to `<project_root>/corpus/<book_name>/antigravity/<page_number>.jsonl`
   - Use `write_to_file` to create the file

7. **Show the report** to the user via `notify_user`, including:
   - The RAPPORT section
   - Number of pairs extracted
   - Path to the saved JSONL file
   - Any observations about prompt coverage gaps
