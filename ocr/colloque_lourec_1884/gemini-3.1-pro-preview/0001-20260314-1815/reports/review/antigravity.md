# Quality Review — colloque_lourec_1884

> **Reviewer**: Antigravity (LLM-as-Judge)
> **Date**: 2026-03-15
> **Run**: `0001-20260314-1815`
> **Model**: `gemini-3.1-pro-preview`
> **Corpus**: 4,141 pairs (3,954 unique) across 72 JSONL files — **the largest book in the pipeline**

---

## 1. Overall Assessment

| Metric | Value |
|--------|-------|
| Pages in report | 71 / 71 |
| JSONL files | 72 (page 01 title page dropped) |
| Total pairs (raw) | 4,141 (avg 57.5/page) |
| Unique pairs | 3,954 (143 cross-page duplicates) |
| Self-reported score | 100% on all 71 pages |
| Pair validity rate | **~99.9%** |
| Pair value rate | **~95%** (section headers + repeated dialogue forms) |
| Print defect handling | ✅ `Por -Louis.` excluded for missing 't' |
| Inverted translation handling | ✅ 2 lines on p56 correctly excluded |
| Truncation handling | ✅ Cross-page truncated phrases excluded throughout |
| Suspension point exclusion | ✅ Mid-phrase `...` excluded; end-of-phrase `...` preserved |
| Synonym splitting | ✅ `ou`/`,` variants consistently split |
| Parenthetical notes | ✅ Disambiguations removed per prompt |
| Column reversal | ✅ FR left / BR right correctly handled on pp. 2-3 |

**Verdict: Excellent quality.** This is the largest and most stylistically varied book — 4-column vocabulary, short dialogues, long letters, geographical lists, and a table of contents. The extraction handles all formats consistently.

---

## 2. Book Characteristics

| Feature | Complexity |
|---------|-----------|
| **4-column vocabulary** | BR1\|FR1\|BR2\|FR2 — each pair independently |
| **Short dialogues** | Numbered sections (I–XXXV+), phrase-by-phrase |
| **Long prose letters** | Schoolboy letters, commercial letters, sentence splitting |
| **Geographical lists** | 100+ Finistère/Morbihan/Côtes-du-Nord city names |
| **Table of contents** | Bilingual section titles with page numbers stripped |
| **Column reversal (pp. 2-3)** | FR left, BR right — publisher's preface |
| **Suspension points** | Fill-in-blank patterns (`...` mid-phrase) excluded |
| **Print defects** | Missing letters, inverted translations |

---

## 3. Cross-Page Duplicate Analysis

143 pairs appear on multiple pages (187 extra entries). Top duplicates:

| Pair | Count | Reason |
|------|-------|--------|
| `Autrou → Monsieur` | 14 | Dialogue form of address |
| `Dialog. → Dialogue.` | 13 | Section header |
| `Ia, autrou. → Oui, monsieur.` | 11 | Polite response in every dialogue |
| `Ne vanquin quet. → Je n'y manquerai pas.` | 5 | Common closing formula |
| `Dialog → Dialogue` | 4 | Variant without period |
| `eur Bluen → une Plume` | 3 | Vocabulary word |
| `Itroun → Madame` | 3 | Form of address |
| `Manific. → Fort bien.` | 3 | Common reply |
| `Quenavezo, autrou. → Adieu, monsieur.` | 3 | Closing formula |
| ... (134 more) | 2 each | Various |

**Assessment**: High duplication is expected for a **phrasebook with 35+ dialogue sections**. The forms of address (`Autrou`, `Itroun`), section headers (`Dialog.`), and common replies (`Ia, autrou.`) naturally repeat. Deduplication at corpus stage recommended.

---

## 4. Print Defect Handling

| Page | Issue | Action | Verdict |
|------|-------|--------|---------|
| p56 | 2 lines with inverted BR translations at printing | Excluded both | ✅ Astute detection |
| p68 | `Por -Louis.` (missing 't' → should be `Port-Louis`) | Excluded | ✅ Per "ne pas deviner" rule |
| p57 | `En v ulez-vous` (coquille preserved) | Kept | ✅ Faithful transcription |
| p70 | `Prènvetj` and `co.njugueson` | Excluded | ✅ Manifestly broken words |

---

## 5. Tricky Pages — LLM-as-Judge Deep Review

### Page 56 (pp. 110–111) — 56 pairs | Inverted Print Translations

**Challenge**: Two lines on p110 have Breton translations **swapped at the printing stage**: `Allez à la poste.` paired with `Ac'hano e terit-hu?` ("Are you coming from there?") and `En venez-vous?` paired with `It d'ar post.` ("Go to the post").

| Check | Result |
|-------|--------|
| 2 inverted lines excluded | ✅ Both correctly identified and removed |
| Dialogue XXXIII continuation | ✅ 22 pairs, all well-aligned |
| Dialogue XXXIV (cloth buying) | ✅ 10 pairs, prices and quantities correct |
| Dialogue XXXV (hat buying) | ✅ Complete exchange extracted |
| **Match** | **56/56 — 100%** |

---

### Page 67 (pp. 132–133) — 76 pairs | Place Names + Synonym Splitting

**Challenge**: Dense geographical list of Finistère cities/towns/islands with `(Kerne)` / `(Leon)` parenthetical notes and `ou` synonyms in port names.

| Check | Result |
|-------|--------|
| Truncated paragraph at top of p132 | ✅ Excluded |
| Section title | ✅ `Hanoiou ar c'herriou principala Vreiz...` |
| `da Goncq → à Concarneau` and `da Goncq → au Conquet` | ✅ Two distinct cities with `(Kerne)` / `(Leon)` stripped |
| `da Locornan (ar Fanq.) → à Saint-Renan` | ✅ Correct — Breton name for Saint-Renan is `Loc-Ronan-ar-Fank` |
| `Rade de Roscoff ou le chenal de l'Ile-de-Batz` split | ✅ Two entries per synonym rule |
| Islands section | ✅ 4 islands correctly paired |
| Rades/ports | ✅ 9 geographical features |
| **Match** | **76/76 — 100%** |

---

### Page 02 (pp. 2–3) — 8 pairs | Reversed Columns + Long Text

**Challenge**: Publisher's preface ("AVIS DE L'ÉDITEUR / ALI AR HOMPOSER") with **French on the LEFT and Breton on the RIGHT** — reversed from the rest of the book.

| Check | Result |
|-------|--------|
| Column reversal detected | ✅ Breton first in all JSONL entries |
| Title pair | ✅ `ALI AR HOMPOSER → AVIS DE L'ÉDITEUR` |
| Sentence-by-sentence alignment | ✅ 7 content pairs, well-aligned |
| Truncated last paragraph | ✅ Excluded (continues on next page) |
| Long compound sentences | ✅ #8 is a 50+ word sentence, correctly aligned |
| **Match** | **8/8 — 100%** |

---

### Page 68 (pp. 134–135) — 65 pairs | Missing Print Letter

**Challenge**: Last geography page — Morbihan, Ille-et-Vilaine, Loire-Inférieure departments. `Port-Louis` printed with missing 't' as `Por.-Louis.`.

| Check | Result |
|-------|--------|
| `Por.-Louis.` / `Porz-Loiz` excluded | ✅ Missing letter, cannot guess |
| Department headers as pairs | ✅ 4 department names extracted |
| Island continuation from p67 | ✅ 19 more island entries |
| Côtes-du-Nord cities | ✅ 13 city pairs |
| Morbihan cities | ✅ 11 city pairs |
| Ille-et-Vilaine cities | ✅ 7 city pairs |
| Loire-Inférieure cities | ✅ 9 city pairs |
| Dialog intro sentences | ✅ `Vademezel...` / `Autrou...` |
| FIN marker excluded | ✅ |
| **Match** | **65/65 — 100%** |

---

### Page 60 (pp. 118–119) — 19 pairs | Long Letters + Truncated Phrases

**Challenge**: Transition to letter-writing section with long prose paragraphs. Cross-page truncation, `...` mid-sentence exclusion, and multi-sentence paragraphs requiring splitting.

| Check | Result |
|-------|--------|
| Dialog continuation (p118 top) | ✅ 7 short pairs correctly extracted |
| `En azrouez ar... dirag ti an...` (mid-`...`) | ✅ Excluded per prompt rule |
| Letter title | ✅ `Lizer eur scolaer d'he dad. → Lettre d'un écolier à son père.` |
| Long sentence splitting | ✅ #10 and #11 each map a full paragraph |
| Closing formula with `...` at end | ✅ Preserved (`ha merc'h...`, `mab haservicher...`) |
| Truncated sentence at p119 bottom | ✅ Excluded (letter continues on next page) |
| Section title for next letter | ✅ #19: `Lizer da bedi eur Mignoun evit eur C'hefridi.` |
| **Match** | **19/19 — 100%** |

---

### Summary of Re-extraction

| Page | Pairs | Match | Key Challenge |
|------|-------|-------|---------------|
| p56 | 56 | 100% | 2 inverted print translations excluded |
| p67 | 76 | 100% | Place names, synonym splitting, parenthetical notes |
| p02 | 8 | 100% | Reversed column order (FR left, BR right) |
| p68 | 65 | 100% | Missing print letter, geography across 4 departments |
| p60 | 19 | 100% | Long prose letters, truncation, mid-`...` exclusion |
| **Total** | **224** | **100%** | |

---

## 6. Content Type Distribution

| Category | Count | % | Description |
|----------|-------|---|-------------|
| **Vocabulary pairs** | ~1,400 | 34% | 4-column word lists (professions, nature, grammar) |
| **Dialogue phrases** | ~1,800 | 43% | 35+ numbered dialogue sections |
| **Place names** | ~180 | 4% | Cities, ports, islands, departments |
| **Letters/prose** | ~200 | 5% | Long paragraph-aligned sentences |
| **Section headers** | ~160 | 4% | `Dialog.`, `Ar Masson → Le Maçon`, TOC entries |
| **Table of contents** | ~100 | 2% | Chapter titles (Roman numerals stripped) |
| **Verb lists** | ~300 | 7% | Infinitives in parallel columns |

---

## 7. Prompt Assessment

### Book Prompt (`colloque_lourec_1884.md`)

**Strengths (135 lines — highly detailed):**
- Exhaustive rules for every content type (vocabulary, dialogues, letters, TOC, geography)
- Explicit handling of `...` mid-sentence vs end-of-sentence
- Column reversal for pp. 2-3 clearly documented
- Synonym splitting with `ou` and `,` — well-defined with examples
- Parenthetical note removal with clear examples
- Dash cadratin (`—`) substitution rule for lexique section categories
- Grammar word exclusion rule with concrete examples
- TOC extraction with Roman numeral and page number stripping

**Minor observations:**
1. **`Dialog.` duplication**: `Dialog.` appears 13x as a section header. The prompt says to extract profession titles as lexical pairs, and `Dialog.` qualifies. Could be excluded at corpus stage.
2. **`Autrou → Monsieur` duplication**: 14x as a dialogue form of address. These ARE legitimate bilingual pairs but repetitive.
3. **No issues detected** with the prompt's actual rules — all edge cases are well-covered.

---

## 8. Final Verdict

| Category | Rating | Notes |
|----------|--------|-------|
| **Accuracy** | ⭐⭐⭐⭐⭐ | 100% match on all 5 re-extracted pages |
| **Completeness** | ⭐⭐⭐⭐⭐ | All content types extracted comprehensively |
| **Print Defects** | ⭐⭐⭐⭐⭐ | Inverted translations, missing letters — all handled |
| **Truncation** | ⭐⭐⭐⭐⭐ | Cross-page truncations consistently excluded |
| **Suspension Points** | ⭐⭐⭐⭐⭐ | Mid-phrase `...` excluded, end-phrase `...` preserved |
| **Column Reversal** | ⭐⭐⭐⭐⭐ | Correctly handled for pp. 2-3 |
| **Synonym Splitting** | ⭐⭐⭐⭐⭐ | `ou` and `,` variants consistently split |
| **Prompt Quality** | ⭐⭐⭐⭐⭐ | Most comprehensive prompt in the pipeline (135 lines) |
| **Pair Value** | ⭐⭐⭐⭐ | Rich but ~4.5% redundancy from dialogue forms |
| **Overall** | **⭐⭐⭐⭐⭐** | **Production-ready. Best quality in the pipeline so far.** |

### Action Items (optional)

1. **Corpus stage**: Deduplicate dialogue forms (`Autrou → Monsieur`, `Ia, autrou.` etc.)
2. **Corpus stage**: Deduplicate section headers (`Dialog.`, `Dialogue.`)
3. **Consider**: Place name pairs (`da Goncq → à Concarneau`) are excellent vocabulary but may deserve a separate corpus tag for geo-linguistic research
