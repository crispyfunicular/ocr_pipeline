# OCR Extraction Quality Review

| Field            | Value                                                  |
|------------------|--------------------------------------------------------|
| **Book**         | le_gonidec_vocabulaire_1919                            |
| **Model**        | gemini-3.1-pro-preview                                 |
| **Run**          | 0001-20260314-1826                                     |
| **Reviewer**     | LLM-as-Judge (Antigravity)                             |
| **Date**         | 2026-03-16                                             |
| **Pages reviewed** | 6 / 299 (p80, p114, p139, p200, p221, p298)          |

---

## 1 · Corpus-Level Statistics

| Metric                        | Value   |
|-------------------------------|---------|
| Total JSONL files             | 299     |
| Pages with pairs              | 298     |
| Pages with 0 pairs            | 1 (p221)|
| Total pairs (raw)             | 35,196  |
| Unique pairs                  | 34,431  |
| Cross-page duplicates         | 701     |
| Malformed JSON lines          | 1       |
| Short entries (breton ≤ 2 ch) | 128     |
| Em-dash residuals             | **0**   |
| `fig.` in values (contextual) | ~227 (legitimate dictionary "au fig." annotations) |
| Pair count / page: min        | 0       |
| Pair count / page: max        | 173     |
| Pair count / page: avg        | 117.7   |
| Pair count / page: stddev     | 24.2    |

---

## 2 · Page-Level Deep Reviews

### 2.1 · Page 298 — Lowest pair count (4 pairs)

**Image**: Supplement page at end of book (pages 582–583). Contains only a few lines of addenda entries.

| Check                  | Result | Notes |
|------------------------|--------|-------|
| Pair count plausible   | ✅     | Only 4 entries visible on the supplement page |
| Breton accuracy        | ✅     | `deoliadur`, `dibuniñ`, `diweriñ`, `trevadennoù` all correct |
| French accuracy        | ✅     | `désolation`, `déposer (un roi)`, `guérir`, `aventures` all correct |
| Em-dash resolved       | N/A    | No em-dashes on this page |
| Normalization          | ✅     | Clean Unicode, proper diacritics |

**Verdict**: ✅ **No issues.** Low pair count is contextually correct — this is the final supplement page.

---

### 2.2 · Page 114 — Highest pair count (173 pairs)

**Image**: Two-column dense dictionary spread (pages 202–203), range *éme–émo* / *émo–emp*.

| Check                  | Result | Notes |
|------------------------|--------|-------|
| Pair count plausible   | ✅     | Very dense page with many synonym expansions |
| Breton accuracy        | ✅     | Spot-checked: `estlammi`, `soueza`, `displega`, `diskleria`, `stambouc'h` all correct |
| French accuracy        | ✅     | `émerveiller`, `émettre`, `exprimer`, `empêcher`, `emphase` all correct |
| Synonym expansion      | ✅     | Correctly creates separate pairs for each Breton synonym (e.g., 4 pairs for "émettre") |
| Em-dash resolved       | ✅     | `empêcher de (faire)` properly expanded, no raw em-dashes |
| Normalization          | ✅     | Unicode consistent, diacritics preserved |

**Observations**:
- Some entries show good French contextual segmentation: e.g., `"empêcher de"` with distinct Breton translations `"herzel ouz"`, `"mirout ouz a"`, `"mirout ouz da"`.
- Gender/grammar markers correctly excluded from translation fields.

**Verdict**: ✅ **No issues.** High pair count is justified by the density of the source material.

---

### 2.3 · Page 139 — Known issue (malformed JSON)

**Image**: Two-column dictionary spread (pages 252–253), range *fram–fray* / *frei–frét*.

| Check                  | Result | Notes |
|------------------------|--------|-------|
| Total lines            | 125    | 124 valid + 1 malformed |
| Malformed line         | 🔴     | **L41**: `{"français": "union fraternelle", "breudeuriez"}` — missing `"breton":` key |
| Breton accuracy        | ✅     | `flamboez`, `gwirion`, `krenn`, `tremenout`, `skei` all correct |
| French accuracy        | ✅     | `framboise`, `franc`, `franchir`, `frapper` all correct |
| Synonym expansion      | ✅     | Multiple Breton words per French headword properly separated |

**Issue detail — L41**:
```json
// ❌ Actual (malformed)
{"français": "union fraternelle", "breudeuriez"}

// ✅ Expected
{"breton": "breudeuriez", "français": "union fraternelle"}
```

The VLM produced a bare string `"breudeuriez"` instead of a proper key-value pair. The Breton word is clearly identifiable from context (the image shows: *fraternelle, breudeuriez, f.*).

**Verdict**: 🔴 **1 critical issue.** Single malformed JSON line — easily fixable.

---

### 2.4 · Page 80 — Random sample (125 pairs)

**Image**: Two-column dictionary spread (pages 134–135), range *cous–couv* / *crab–cras*.

| Check                  | Result | Notes |
|------------------------|--------|-------|
| Pair count plausible   | ✅     | Dense two-page spread, 125 pairs reasonable |
| Breton accuracy        | ✅     | `kenderv`, `kontell`, `kousta`, `koustout`, `strakal` all correct |
| French accuracy        | ✅     | `cousin`, `couteau`, `coûter`, `craquer`, `crasse` all correct |
| Pronominal verb norm.  | ✅     | `"se cramponner"` correctly expanded |
| Em-dash resolved       | ✅     | No raw em-dashes present |
| Contextual splitting   | ⚠️     | `"du corps ou du visage"` for `"vilgen"` and `"ounezer"` — these are sub-entries under *crasse* and should ideally include the headword |

**Observations**:
- Entry `{"breton": "vilgen", "français": "du corps ou du visage"}` — the French field lost context. The image shows these as sub-meanings of *crasse* (crasse du corps ou du visage). However, this is a known pattern with sub-entries in this dictionary, and the adjacent entry `{"breton": "koc'hienn", "français": "crasse"}` provides the headword, so the pair remains partially useful.

**Verdict**: ⚠️ **1 minor issue** — occasional loss of headword context in sub-entries, but not a critical defect.

---

### 2.5 · Page 200 — Random sample (117 pairs)

**Image**: Two-column dictionary spread (pages 374–375), range *océ–off* / *off–omeg*.

| Check                  | Result | Notes |
|------------------------|--------|-------|
| Pair count plausible   | ✅     | Dense two-page spread, 117 pairs reasonable |
| Breton accuracy        | ✅     | `mor-bras`, `eizved`, `mezeg-dremm`, `louzaouer an daoulagad` all correct |
| French accuracy        | ✅     | `océan`, `octave`, `oculiste`, `omission` all correct |
| Em-dash resolved       | ✅     | No raw em-dashes present |
| Contextual refinement  | ✅     | `"ombrageux (animal)"` vs `"ombrageux (personne)"` correctly differentiated |
| Compound entries       | ✅     | `"omettre par oubli"` / `"omettre par négligence"` correctly split |
| Pronominal verbs       | N/A    | No pronominal verbs on this page |

**Observations**:
- Good handling of context disambiguation: `"témoin oculaire"`, `"de l'œil"` properly extracted with relevant Breton words.
- `"ombre d'un mort"` / `"ombre d'un tableau"` correctly differentiated — strong prompt compliance.

**Verdict**: ✅ **No issues.** Excellent extraction quality.

---

### 2.6 · Page 221 — False Impossible (0 pairs)

**Image**: Image exists at `pages_enhanced/le_gonidec_vocabulaire_1919/221.jpg`. It is a standard two-column dictionary page.

| Check                  | Result | Notes |
|------------------------|--------|-------|
| Image present          | ✅     | File exists and is a valid dictionary page |
| JSONL content          | 🔴     | **Empty file** — 0 pairs extracted |
| Extraction report      | 🔴     | Marked "Impossible" — but page is clearly extractable |
| Root cause             | 🔴     | API 429 errors (RESOURCE_EXHAUSTED) caused retry failures; page was incorrectly classified |

**Root cause analysis**:
The extraction report shows page 221 was attempted twice and received `429 RESOURCE_EXHAUSTED` errors both times. The pipeline then classified it as "Impossible" instead of recognizing the API quota error as a transient failure. This is a **pipeline logic issue** — API rate-limit errors should be classified as retriable errors, not as impossible pages.

**Verdict**: 🔴 **Critical — lost page.** An entire dictionary page (~100+ pairs estimated) was not extracted. Requires re-extraction.

---

## 3 · Book-Specific Prompt Compliance

| Rule                                   | Status | Evidence |
|----------------------------------------|--------|----------|
| Em-dash resolution (— → headword)      | ✅     | 0 residual em-dashes across all 35,196 pairs |
| Pronominal verb normalization           | ✅     | `se cramponner`, `s'émerveiller` properly extracted |
| `fig.` abbreviation handling            | ✅     | `fig.` appears only in legitimate dictionary context ("au fig.") — not as unresolved abbreviation |
| Breton grammar exclusion from French    | ✅     | Gender markers (m., f.) and grammatical notes excluded from pair values |
| Truncated first-letter reconstruction   | ✅     | No truncated entries observed in sampled pages |
| Synonym expansion (one pair per word)   | ✅     | Consistently applied across all reviewed pages |
| Cross-reference handling                | ✅     | `v.` references appropriately treated |

---

## 4 · Issue Summary

### 🔴 Critical Issues

| # | Page | Description | Impact | Fix |
|---|------|-------------|--------|-----|
| C1 | p221 | **False Impossible**: entire page not extracted due to API 429 errors misclassified as "Impossible" | ~100+ pairs lost | Re-extract page 221 |
| C2 | p139, L41 | **Malformed JSON**: `{"français": "union fraternelle", "breudeuriez"}` — missing `"breton":` key | 1 pair unusable | Fix JSON manually or re-extract |

### ⚠️ Warnings

| # | Scope | Description | Impact |
|---|-------|-------------|--------|
| W1 | Corpus-wide | **701 cross-page duplicates** (~2.0% of total). Some are legitimate (common words appear in multiple dictionary entries), but volume warrants sampling. | Minor — filtering at corpus build time |
| W2 | Sparse | **Sub-entry context loss**: some sub-meanings lose their headword context (e.g., `"du corps ou du visage"` without `"crasse"`). | Minor — affects ~1-2% of entries |
| W3 | Sparse | **128 short entries** (breton ≤ 2 chars). Many are legitimate single-letter entries or abbreviations. | Low — needs manual sampling |

### ℹ️ Informational

| # | Scope | Description |
|---|-------|-------------|
| I1 | Corpus | `fig.` appears in ~227 entries as legitimate "au fig." annotations — **not** abbreviation residuals |
| I2 | p298 | Only 4 pairs — correct for a supplement/addenda page |
| I3 | Pipeline | Multiple 429 errors during extraction suggest aggressive API request rate |

---

## 5 · Scoring

| Dimension                | Score | Notes |
|--------------------------|-------|-------|
| **Accuracy**             | 9/10  | Breton and French words highly accurate across all sampled pages |
| **Completeness**         | 8/10  | 1 full page lost (p221), otherwise comprehensive coverage |
| **Normalization**        | 10/10 | Zero em-dash residuals, proper Unicode, proper pronominal verbs |
| **Prompt compliance**    | 9/10  | All book-specific rules followed; minor sub-entry context loss |
| **Data integrity**       | 9/10  | Only 1 malformed line across 35,196 pairs (0.003%) |
| **Overall**              | **9/10** | Excellent extraction quality with 2 actionable fixes needed |

---

## 6 · Recommendations

1. **Re-extract page 221** — the image is valid and contains standard dictionary content.
2. **Fix p139 L41** — correct the malformed JSON line to `{"breton": "breudeuriez", "français": "union fraternelle"}`.
3. **Pipeline improvement** — classify API 429/RESOURCE_EXHAUSTED errors as retriable rather than marking the page as "Impossible". Consider adding exponential backoff with longer delays for quota exhaustion.
4. **Cross-page dedup strategy** — during corpus assembly, consider deduplication rules that preserve the most complete context when the same pair appears on multiple pages.
