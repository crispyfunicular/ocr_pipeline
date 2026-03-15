---
description: Critically review local uncommitted or staged changes (git diff review)
---

# Review Local Changes

A thorough, critical review of local git changes — mimicking a senior engineer's code review.

CRITICAL RULE: NEVER perform any write action on GitHub without explicit user permission. This includes but is not limited to: submitting PR reviews, posting comments, creating/merging pull requests, pushing commits, creating branches, or creating issues. Always draft the content locally and present it to the user for review and approval BEFORE publishing anything to GitHub.

## When to Use

- Before committing, to catch issues early
- When the user asks to review changes, review diff, review local changes, etc.
- Invoked via `/review-changes`

## Steps

### 1. Determine the scope

Run one of the following based on user intent:

```bash
# Unstaged changes
git diff

# Staged changes
git diff --cached

# All local changes (staged + unstaged) vs HEAD
git diff HEAD

# Changes on branch vs main/master
git diff main...HEAD
```

// turbo-all

If the user doesn't specify, default to `git diff HEAD` (all uncommitted changes).

If the diff is very large (>500 lines), use `git diff HEAD --stat` first to get an overview, then review files individually with `git diff HEAD -- <path>`.

### 2. Review each changed file

For every modified file, evaluate against ALL of the following checklist:

#### Correctness
- [ ] Does the logic do what it claims?
- [ ] Are edge cases handled (None, empty lists, missing files, missing dirs)?
- [ ] Are error paths correct (proper sys.exit, no swallowed exceptions)?
- [ ] Are there race conditions or thread-safety issues?

#### Consistency
- [ ] Does the change follow existing patterns in the codebase?
- [ ] Are naming conventions consistent (snake_case everywhere, no stale `preprocess`/`--books` refs)?
- [ ] Does it match the code style of surrounding files?
- [ ] Is the `main(argv=None)` pattern preserved for pipeline-callable scripts?

#### Completeness
- [ ] Are all necessary files modified (scripts, pipeline.py, docs)?
- [ ] Are there TODO/FIXME left behind unintentionally?
- [ ] Did the change update ARCHITECTURE.md / AGENTS.md / README.md if needed? (per project rules)
- [ ] Are imports clean (no unused, no missing)?
- [ ] If a script was renamed, are all references updated (pipeline.py, docs, examples)?

#### Robustness
- [ ] Is stdout vs stderr usage correct? (errors to stderr, progress to stdout)
- [ ] Are file paths handled with `Path` objects, not string concatenation?
- [ ] Are resources properly cleaned up (file handles, GPU memory, API connections)?
- [ ] Does the code handle missing PDFs / empty directories / corrupt images gracefully?

#### Security
- [ ] Are there hardcoded API keys or credentials?
- [ ] Is `OPENAI_API_KEY` read from env, never logged or printed?
- [ ] Are there path traversal risks in user-supplied targets?

#### Pipeline Integration
- [ ] Does `pipeline.py` correctly forward args to sub-scripts via `--targets`?
- [ ] Does the `run` command chain stages correctly with sanitized book names?
- [ ] Are positional `targets` consistent across all subcommands?
- [ ] Is the `[] or None` bug pattern avoided? (always use explicit `is None` checks)

#### Prompts & OCR Quality
- [ ] Are VLM prompts (French) preserved without accidental modification?
- [ ] Are prompt file paths correct (looking in `prompts/` directory)?
- [ ] Are JSONL output fields consistent with the expected schema?

#### Prompt Review Deep-Dive (when `prompts/*.md` files are in the diff)

Skip this section entirely if no files under `prompts/` are modified.

**Semantic Impact**
- [ ] Does the change contradict or weaken an existing extraction rule?
- [ ] Does it introduce ambiguity the LLM could misinterpret? (vague wording, double negations, implicit assumptions)
- [ ] Are the "extract" and "exclude" sections still logically consistent with each other?
- [ ] Does the change unintentionally broaden or narrow the scope of extraction?

**Cross-Prompt Consistency** (`extract_bilingual_corpus.md` ↔ per-book `prompts/<book>.md`)
- [ ] If a rule was added/changed in the base prompt, do per-book prompts still make sense? (no conflicts, no stale overrides)
- [ ] If a per-book prompt was changed, does it duplicate or contradict the base prompt?
- [ ] Is the layering correct? (per-book prompts should only add book-specific rules, not restate generic ones)

**Example Validation**
- [ ] Are all JSON examples in the prompt syntactically valid JSONL? (`{"breton": "...", "français": "..."}`)
- [ ] Do examples actually demonstrate the rules they illustrate? (no mismatch between rule text and example)
- [ ] Are there examples covering the newly added/changed rules?
- [ ] Are negative examples (what NOT to extract) provided where the rule is subtle?

**Regression Risk**
- [ ] Could this change cause previously correct extractions to be rejected? (tightened rules)
- [ ] Could this change cause previously excluded content to be extracted? (loosened rules)
- [ ] If high risk: recommend re-running 1-2 pages with `--limit 1 --debug` on an affected book to spot-check

**LLM Clarity & Structure**
- [ ] Is the prompt in clear, unambiguous French?
- [ ] Are rules ordered by priority? (critical rules like alignment and fidelity first)
- [ ] Are section headers and formatting consistent with the rest of the prompt?
- [ ] Is the prompt length still reasonable? (excessive length can degrade LLM attention to later rules)

#### Documentation (README.md, AGENTS.md, ARCHITECTURE.md, `--help`)
- [ ] Do user-facing docs reflect the new/changed behavior?
- [ ] Are CLI examples up-to-date and copy-paste ready?
- [ ] Are options/flags documented consistently with `--help` output?
- [ ] Does ARCHITECTURE.md data flow diagram reflect the current pipeline?
- [ ] Does README.md usage section cover new CLI flags, subcommands, or changed defaults?

**AGENTS.md vs ARCHITECTURE.md separation** — these two docs serve different audiences and must not duplicate each other:

| | **AGENTS.md** | **ARCHITECTURE.md** |
|---|---|---|
| **Audience** | AI coding assistants/agents | Humans (developers, contributors) |
| **Purpose** | Quick-reference cheat sheet for editing the code safely | Complete system design documentation |
| **Contains** | Entry points table, coding conventions & gotchas, environment setup, file map | Data flow diagrams, stage-by-stage details, schema definitions, quality metrics, roadmap |
| **Tone** | Imperative rules ("always do X", "never do Y") | Descriptive documentation ("the system does X") |

Rules for keeping them clean:

- [ ] **No system details in AGENTS.md**: AGENTS.md should never describe *how* a feature works internally (e.g., batch API flow, ThinkingConfig wiring). Cross-reference ARCHITECTURE.md instead.
- [ ] **No agent gotchas in ARCHITECTURE.md**: ARCHITECTURE.md should not contain agent-specific warnings like "always pass `[]` not `None`". Those belong in AGENTS.md.
- [ ] **Facts live in one place**: if a fact (e.g., run_state.json schema, folder naming convention) is documented in ARCHITECTURE.md, AGENTS.md should reference it, not restate it.
- [ ] **Entry points table is AGENTS.md-only**: the CLI command table with copy-paste examples lives in AGENTS.md (and README.md for users). ARCHITECTURE.md describes the stages conceptually.
- [ ] **Test counts in AGENTS.md are accurate**: when adding tests, update the counts in AGENTS.md's Important Files section.

### 3. Cross-check with project context

- Read ARCHITECTURE.md and AGENTS.md
- Verify the change aligns with documented patterns
- Check if any of these docs need updating, respecting the separation rules above

### 4. Lint and syntax check

Only if there are code changes:

```bash
source .venv/bin/activate && python -m py_compile pipeline.py 2>&1
```

```bash
for f in src/*.py src/ocr/*.py; do python -m py_compile "$f" 2>&1; done
```

```bash
black --check pipeline.py src/ tests/ 2>&1
```

### 5. Run unit tests

If there are code changes, run the full test suite (fast, no GPU/API needed):

```bash
make test
```

All tests must pass. If any fail, flag them as 🔴 Critical issues.

### 6. Smoke test

If there are code changes, run a quick smoke test:

```bash
source .venv/bin/activate && python pipeline.py --help 2>&1
python pipeline.py extract --help 2>&1
python pipeline.py enhance --help 2>&1
python pipeline.py ocr --help 2>&1
python pipeline.py corpus --help 2>&1
```

### 7. Produce the review report

Structure the output as:

```markdown
## Review Summary

**Scope**: <what was reviewed, e.g. "3 files, 47 insertions, 12 deletions">
**Verdict**: ✅ LGTM / ⚠️ Minor issues / ❌ Changes requested

## Issues Found

### 🔴 Critical (must fix)
- [file:line] Description of the issue

### 🟡 Suggestions (should fix)
- [file:line] Description of the suggestion

### 🔵 Nits (optional)
- [file:line] Description of the nit

## What Looks Good
- Brief mention of things done well

## Checklist
- [ ] Compiles clean
- [ ] Tests pass (`make test`)
- [ ] CLI help works
- [ ] Docs updated
- [ ] ARCHITECTURE.md in sync
- [ ] AGENTS.md in sync
```

### 8. Offer to fix issues

If issues are found, ask the user:
> Would you like me to fix the [critical/suggested] issues?

Do NOT auto-fix without asking. Present the findings first, let the user decide.

## Important Notes

- Be genuinely critical — the goal is to catch bugs before they ship
- Don't just rubber-stamp changes with "LGTM" unless they're truly clean
- Pay special attention to: stale references after renames, argv forwarding bugs, missing Path handling, prompt corruption
- If a change seems incomplete (e.g., missing doc updates for new behavior), flag it
- Compare against ARCHITECTURE.md and AGENTS.md and project conventions