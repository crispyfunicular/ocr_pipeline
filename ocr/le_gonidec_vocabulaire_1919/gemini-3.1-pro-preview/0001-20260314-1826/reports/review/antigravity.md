# Quality Review — le_gonidec_vocabulaire_1919

> **Reviewer**: Antigravity (LLM-as-Judge)
> **Date**: 2026-03-15
> **Run**: `0001-20260314-1826`
> **Model**: `gemini-3.1-pro-preview`
> **Corpus**: 35,197 pairs (34,431 unique) across 298 JSONL files — **by far the largest book in the pipeline**

---

## 1. Overall Assessment

| Metric | Value |
|--------|-------|
| Pages in report | 298 OK + 1 Impossible (p221) + 137 retried errors |
| JSONL files | 298 |
| Total pairs (raw) | 35,197 (avg 118/page) |
| Unique pairs | 34,431 (715 cross-page duplicates) |
| Malformed JSON lines | **1** (`139.jsonl:41` missing `"breton":` key) |
| Self-reported score | avg 100%, min 95%, max 100% |
| Extraction cost | $12.94 ($0.030/page) |
| Em-dashes in French fields | **0** ✅ |
| Abbreviation residuals | 3 (borderline — `subst.`/`adj.` used in French context) |
| Short entries (≤2 chars Breton) | 128 (all legitimate: tu, ti, ro, hi, a, etc.) |
| Print defect handling | ✅ "babit" faithfully preserved |
| Truncation handling | ✅ Cross-page truncated entries excluded |
| Synonym splitting | ✅ Consistent across 298 pages |
| Dash resolution | ✅ Zero unresolved em-dashes in 35K pairs |

**Verdict: ⭐⭐⭐⭐½ — Excellent with 2 actionable issues.**

---

## 2. Actionable Issues

### 🔴 Issue 1: p221 — False "Impossible"

Page 221 (pp. 416–417, section pré-/préc-) was classified as **Impossible** with 0 pairs extracted — but visual inspection confirms it is a perfectly normal, dense dictionary page with ~40+ extractable entries. The page was first hit by a 429 rate limit, then upon retry produced "Impossible" after 468s / $0.046 of processing (tokens consumed but nothing output).

**Impact**: ~100–120 missing pairs (pre-/préc- section entries).
**Action**: Re-extract page 221 only.

### 🟡 Issue 2: Malformed JSON in 139.jsonl

Line 41 of `139.jsonl` contains:
```json
{"français": "union fraternelle", "breudeuriez"}
```
Missing `"breton":` key. Should be:
```json
{"français": "union fraternelle", "breton": "breudeuriez"}
```

**Impact**: 1 lost pair.
**Action**: Manual fix or re-extract page 139.

---

## 3. Book Characteristics

| Feature | Description |
|---------|------------|
| **Type** | Full French-Breton dictionary (299 pages, ~600 printed pages) |
| **Layout** | Two-column dictionary, alphabetical A→Z + Supplément |
| **Entries per page** | 46–173 (avg 118) |
| **Sub-entries** | Extensive use of em-dash (`—`) for headword substitution in sub-entries |
| **Synonyms** | Multiple Breton translations per French headword, comma-separated |
| **Abbreviations** | 28 listed abbreviations (m., f., pl., adj., Van., Trég., U.B., etc.) |
| **Margin truncation** | Left margin occasionally cuts first letter of headwords |
| **Supplément** | Pages 590+ contain editorial corrections and phonetic essays |

---

## 4. Cross-Page Duplicate Analysis

715 pairs appear on multiple pages (765 extra entries). This is expected for a dictionary with:
- Cross-referenced entries
- Common verbs appearing in multiple contexts
- Synonyms repeated under different headwords

Top duplicates:

| Pair | Count | Reason |
|------|-------|--------|
| `fréquentation → darempred` | 5 | Cross-referenced from multiple headwords |
| `fréquentation → hentadurez` | 5 | Second synonym, same cross-references |
| `disperser → skigna` | 4 | Common verb |
| `enfoncer → sanka` | 4 | Common verb |
| `parmi → e-touez` | 4 | Common preposition |
| `cacher → kuzat` | 4 | Common verb |
| `répandre → skuilha` | 3 | Common verb |
| `croyance → kredenn` | 3 | Cross-reference |
| ... (706 more) | 2–3 each | Various |

**Assessment**: Well within expected levels for a dictionary of this size. Deduplication at corpus stage recommended.

---

## 5. Tricky Pages — LLM-as-Judge Deep Review

### Page 221 (pp. 416–417) — 0 pairs ❌ | False Impossible

**Challenge**: Normal dictionary page (pré-/préc- section) with 40+ extractable entries including complex sub-entries and abbreviations.

| Check | Result |
|-------|--------|
| Visual inspection | Dense, legible two-column dictionary page |
| Expected pairs | ~100–120 (similar to p222: 163 pairs) |
| Extracted pairs | **0** |
| Model verdict | "Impossible" |
| Root cause | 429 error on first attempt, confusion on retry |
| **Match** | **0/~120 — FAIL** |

---

### Page 125 (pp. 224–225) — 163 pairs ✅ | Highest Density (étr-/évi-)

**Challenge**: Densest page in the corpus. Complex entries with many sub-forms, synonym splitting, and figurative usage annotations.

| Check | Result |
|-------|--------|
| `étrenne` → 2 Breton synonyms | ✅ `kalanna`, `derou-mat` |
| `étrier` → dash resolution: "prendre l'étrier" | ✅ stleuga/stlevia |
| `perdre/quitter l'étrier` → synonym OR split | ✅ Both forms split |
| `étroit` → base + figurative forms | ✅ 6 base synonyms + figurative with qualifiers |
| `eux` entry → grammar word? | ⚠️ Extracted with 11 sub-entries (borderline but useful) |
| `évaporation` + `s'évaporer` → pronominal handling | ✅ Correctly normalized |
| `éveiller`/`s'éveiller` → 13 Breton synonyms | ✅ All split correctly |
| `évidence`/`évident` → separate headwords | ✅ Distinct pairs |
| **Match** | **163/163 — 100%** |

---

### Page 37 (pp. 48–49) — 89 pairs ✅ | Low Count + Complex Entries (bai-/ban-)

**Challenge**: Continuation text from previous page, complex `balance` entry with plurals and sub-entries, truncated final entry.

| Check | Result |
|-------|--------|
| Continuation text at top of p48 excluded | ✅ "per les objets, soub, soubadur..." skipped |
| `baïonnette` → first extracted entry | ✅ 2 Breton synonyms |
| `baiser` → verb + noun forms | ✅ 8 sub-entries including "baisure du pain" |
| `(pain) qui a une —, afedet` → dash resolution | ✅ Resolved to "pain qui a une baisure" |
| `balance` complex entry with plurals | ✅ Correct: 3 main synonyms + sub-entries |
| `bande` at bottom of p49 truncated | ✅ Excluded |
| **Match** | **89/89 — 100%** |

---

### Page 114 (pp. 202–203) — 173 pairs ✅ | Top Pair Count (éme-/emp-)

**Challenge**: Highest pair count of any page. Complex emotion vocabulary, U.B. abbreviation in `empêcher`, and long sub-entry chains.

| Check | Result |
|-------|--------|
| Continuation at top of p202 | ✅ Sub-locution "tendre des embûches" extracted |
| `émettre`/`exprimer` shared synonyms | ✅ Both French senses extracted with same Breton words |
| `émotion` → 12 Breton synonyms | ✅ All split correctly |
| `s'émouvoir` → pronominal | ✅ Correctly normalized |
| `empêcher` + U.B. abbreviation stripped | ✅ "herzel ouz U. B." → "empêcher de → herzel ouz" |
| `empêtrer` → 4 Breton synonyms | ✅ All split |
| **Match** | **173/173 — 100%** |

---

### Page 308 (pp. 590–591) — 25 pairs ✅ | Supplément/Errata

**Challenge**: Not a standard dictionary page — this is the Supplément (corrections & additions). Most content is editorial commentary, long phonetic essays, and correction notes like "Corriger: ..." or "Ajouter: ...".

| Check | Result |
|-------|--------|
| Editorial commentary excluded | ✅ "Ce mot ne se trouve pas dans les textes..." skipped |
| Extractable corrections extracted | ✅ `procédé → trôad`, `prolixe → diresis` |
| Long phonetic essay on p591 excluded | ✅ Not extractable vocabulary |
| `prudence` correction note excluded | ✅ "Supprimer 'gwagellerez'" — meta-commentary |
| `ramier` with complex editorial note | ✅ Only extractable forms: `kudoneta`, `kudona` |
| Sections Q and R headers extracted | ✅ `quatre-cents, quatre-vingts` correct |
| **Match** | **25/25 — 100%** |

---

### Summary of Deep Review

| Page | Pairs | Match | Key Challenge |
|------|-------|-------|---------------|
| p221 | 0 | ❌ FAIL | False Impossible — needs re-extraction |
| p125 | 163 | 100% | Densest page, complex synonym splitting |
| p37 | 89 | 100% | Continuation/truncation + dash resolution |
| p114 | 173 | 100% | Highest count, U.B. abbreviation stripping |
| p308 | 25 | 100% | Supplément errata — editorial vs extractable |
| **Total** | **450** | **100% (excl. p221)** | |

---

## 6. Prompt Assessment

### Book Prompt (`le_gonidec_vocabulaire_1919.md`)

**Strengths (52 lines — well-structured):**
- Em-dash resolution rule with clear example (`voix de baryton`) — **perfectly effective**: 0 remaining dashes in 35K pairs
- Pronominal verb normalization (`accouder (s') → s'accouder`)
- Truncated first-letter reconstruction from alphabetical context
- Comprehensive abbreviation list (28 entries)
- Breton grammar note stripping (plurals, dialectal variants, prepositions)

**No changes recommended.** The prompt handles this enormous dictionary with no gaps.

---

## 7. Final Verdict

| Category | Rating | Notes |
|----------|--------|-------|
| **Accuracy** | ⭐⭐⭐⭐⭐ | 100% on 4/5 reviewed pages |
| **Completeness** | ⭐⭐⭐⭐ | p221 missing (~120 pairs) |
| **Dash resolution** | ⭐⭐⭐⭐⭐ | Zero unresolved in 35K pairs — flawless |
| **Abbreviation cleaning** | ⭐⭐⭐⭐⭐ | 3 borderline residuals out of 35K — excellent |
| **Truncation handling** | ⭐⭐⭐⭐⭐ | Cross-page truncation consistently excluded |
| **Synonym splitting** | ⭐⭐⭐⭐⭐ | Consistent across 298 pages |
| **Prompt quality** | ⭐⭐⭐⭐⭐ | Comprehensive, no gaps identified |
| **Data integrity** | ⭐⭐⭐⭐ | 1 malformed JSON line |
| **Overall** | **⭐⭐⭐⭐½** | **Near-perfect. 2 actionable items before production.** |

### Required Actions

1. ❌ **Re-extract page 221** — false Impossible, ~120 missing pairs
2. 🔧 **Fix `139.jsonl:41`** — add missing `"breton":` key
3. 📊 **Corpus stage**: Deduplicate 715 cross-page duplicates
