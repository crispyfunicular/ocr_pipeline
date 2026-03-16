# Quality Review — yez_hon_tadou_1940

> **Run**: `0001-20260314-1844`
> **Model**: `gemini-3.1-pro-preview`
> **Reviewer**: Antigravity (LLM-as-Judge)
> **Date**: 2026-03-16
> **Pages reviewed**: 5 / 36 (strategy: lowest + highest + flagged + 2 random)
> **Corpus**: 2395 pairs (2248 unique) across 36 JSONL files

## Corpus Stats

| Metric | Value |
|--------|-------|
| Total pairs (raw) | 2395 |
| Unique pairs | 2248 |
| Cross-page duplicates | 120 pairs appearing in >1 file |
| Within-page duplicates | 8 pairs across 6 files |
| Malformed JSON lines | 0 |
| Short entries (≤2 chars) | 5 (all legitimate: `du`/noir, `eo`/est, `ti`/maison, `ki`/chien ×2) |
| Abbreviation residuals | 1 (`ap.` in p77) |
| Unresolved em-dashes | 0 |
| False Impossible pages | 0 |
| Pair count range | 23–112 (avg 66.5, σ 32.7) |

## Page Verdicts

| Page | Pairs | Accuracy | Completeness | Issues |
|------|-------|----------|--------------|--------|
| p12 | 103 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | `composit.` abbreviation kept (faithful to image) |
| p17 | 23 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Within-page duplicate `redek`/`courir` |
| p48 | 93 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 2 within-page dupes (`koadour`, `koadek`) from different sections |
| p64 | 112 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | — |
| p77 | 38 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | `ap. la faim` abbreviation residual |

## Issues

### 🔴 Critical
None

### 🟡 Warning

1. **Abbreviation residual** — p77 line 25: `"terri an naon"` / `"ap. la faim"` — the abbreviation `ap.` should be expanded to `apaiser` (the image shows `ap. la faim` which is itself abbreviated, but the field should read the full form if legible on the page). Alternatively this may be the literal printed text, in which case it's faithful but the abbreviation marker should have been cleaned per normalisation rules.

2. **Within-page duplicates** — 8 duplicate pairs found across 6 files. These arise when a word appears in both the GERIADUR section and the FAMILLE DE MOTS section on the same page:
   - `13.jsonl`: `lenn`/`lire` (×2)
   - `16.jsonl`: `barrek`/`capable` (×2)
   - `17.jsonl`: `redek`/`courir` (×2)
   - `36.jsonl`: `kar`/`parent` (×2)
   - `44.jsonl`: `goañvenn`/`engelure` (×2)
   - `48.jsonl`: `koadour`/`bûcheron` (×2), `koadek`/`boisé` (×2)
   - `60.jsonl`: `flamm`/`frais` (×2)

### 🟢 Info

1. **Cross-page duplicates (120)** — Expected for a language textbook where vocabulary is revisited across lessons. Common repeats include section headers (`Geriadur`/`Vocabulaire`, `Anoiou`/`Noms`), basic vocabulary (`ki`/`chien`, `louet`/`gris`), and verbs reintroduced in later lessons.

2. **Short entries** — All 5 entries with ≤2-character Breton fields are legitimate words: `du` (noir), `eo` (est, sont), `ti` (maison), `ki` (chien ×2).

3. **High pair-count variance** — The standard deviation of 32.7 reflects the book's structure: odd pages tend to have grammar/exercises (fewer pairs: 23–63), while even pages have dense GERIADUR vocabulary lists (81–112 pairs).

4. **Errata application** — The errata correction for `kalz a dud a vary` → `kalz a dud a varv` (p137) was correctly applied in p77 line 37. ✅

5. **Section titles extracted** — Titles like `Geriadur`/`Vocabulaire`, `Anoiou`/`Noms`, `Anoiou - gwan`/`Adjectifs` are extracted as pairs. This is consistent with the global prompt rule to include bilingual titles. However, the book prompt says to **exclude** section titles like `DISPLEGADUR - VERB (Conjugaison)` and `YEZADUR (Grammaire)`. The extracted titles (`Geriadur`/`Vocabulaire`) are vocabulary section headers that serve as valid bilingual pairs, so this is acceptable.

6. **Proper name pairs** — p12 includes `Yannig`/`petit Jean`, `Pêrig`/`petit Pierre`, etc. These are diminutive name translations that are part of the "Noms d'enfants" exercise, and are legitimate bilingual pairs since they demonstrate the Breton diminutive suffix.

## Tricky Page Deep Reviews

### Page 17 (pp. 16–17)

#### Ré-extraction
Paires attendues : ~23 (verb lists only, excluding conjugation table and exercises)
Paires dans le JSONL : 23

#### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1–12 | ✅ | se plaire…jeter | bourra…teurel | 12 verbes mutables — tous corrects |
| 13–21 | ✅ | suer…siffler | c'houezi…sutal | 9 verbes non mutables — corrects |
| 22 | ⚠️ | courir | redek | Duplicate de la ligne 16 (même paire `redek`/`courir`) |
| 23 | ✅ | en courant | o redek | Participe présent — exemple bilingue valide |

#### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| Conjugaison sans traduction → exclure | ✅ | Table "kaout" exclue (forme impersonnelle complexe) |
| Exercices monolingues → exclure | ✅ | Exercices p17 (Poelladennou) correctement ignorés |
| Titres section bilingues → exclure | ✅ | "DISPLEGADUR - VERB (Conjugaison)" exclu |
| YEZADUR (Grammaire) → exclure | ✅ | Section grammaire p17 ignorée |

#### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐ |

#### Problèmes
- 🟡 Within-page duplicate: `redek`/`courir` appears at lines 16 and 22

---

### Page 64 (pp. 110–111)

#### Ré-extraction
Paires attendues : ~112 (dense vocabulary: body parts, adjectives, expressions)
Paires dans le JSONL : 112

#### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1–20 | ✅ | pas…cuisse | kammed…morzed | Noms mutables (masculins + féminins) — tous fidèles à l'image |
| 21–63 | ✅ | l'épaule…le côté | ar skoaz…an tu | Noms sans mutation — transcription fidèle, articles conservés |
| 64–71 | ✅ | abcès au pied…gifle | troadad…skouarnad | Suffixe « -ad » — paires correctes, extraites des exemples |
| 72–99 | ✅ | vivant…maigre | beo…treut | Adjectifs — complets et fidèles |
| 100–112 | ✅ | beau de figure…une belle fille | Dremmet-kaer…eur goantenn a blac'h | Expressions bretonnes — fidèles à l'image |

#### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| Nettoyage marques grammaticales | ✅ | `m.`, `f.`, `iou`, `ou` supprimés dans les champs |
| Articles conservés dans les syntagmes | ✅ | `ar skoaz`/`l'épaule` — articles inclus |
| Noms propres isolés → exclure | ✅ | Aucun nom propre extrait |

#### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐⭐ |

#### Problèmes
- Aucun

---

### Page 12 (pp. 6–7)

#### Ré-extraction
Paires attendues : ~103 (vocabulary lists, proper name translations, famille de mots, adjectives)
Paires dans le JSONL : 103

#### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1 | ✅ | L'Ecole | Ar skol | Titre bilingue — correct |
| 2–3 | ✅ | Vocabulaire, Noms | Geriadur, Anoiou | Section headers — valid bilingual pairs |
| 4–25 | ✅ | cahier…tableau | kaier…taolenn | Noms mutables + paotrez/pajenn/pedenn/taol/taolenn — fidèles |
| 16 | ⚠️ | composit. | kenstrivadenn | Abbreviation `composit.` présent dans le champ FR — mais c'est le texte imprimé sur l'image |
| 26–55 | ✅ | Dieu…la fenêtre | Doue…ar prenestr | Noms sans mutation — transcription complète et fidèle |
| 56–61 | ✅ | petit Jean…petite Marguerite | Yannig…Gaidig | Noms d'enfants — paires de diminutifs valides |
| 62–74 | ✅ | petite école…vacances | Skolig…ehan-skol | Famille de mots « skol » — complète |
| 75–103 | ✅ | Adjectifs…vert | Anoiou - gwan…gwér | Liste d'adjectifs — complète et fidèle |

#### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| Nettoyage marques grammaticales | ✅ | `m.`, `f.`, `iou`, `ed`, `coll.` supprimés |
| Famille de mots → extraire | ✅ | Famille « skol » entièrement extraite |
| Exemples bilingues → extraire | ✅ | Noms d'enfants traités comme paires valides |

#### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐⭐ |

#### Problèmes
- 🟢 `composit.` on line 16 — abbreviation but faithful to printed text on image

---

### Page 48 (pp. 78–79)

#### Ré-extraction
Paires attendues : ~93 (tree vocabulary, collective nouns, famille de mots "koad", adjectives)
Paires dans le JSONL : 93

#### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1 | ✅ | Le bois | AR C'HOAD | Titre bilingue |
| 2–16 | ✅ | tronc…plante | kef…plantenn | Noms mutables — fidèles |
| 17–28 | ✅ | la branche…la scie | ar skourr…an heskenn | Noms sans mutation — articles conservés |
| 29–54 | ✅ | des plantes…broussaille | plant…strouez | Collectifs + arbres — complets |
| 55 | ✅ | un chêne | eun dervenn | Exemple singulier — valide |
| 56–69 | ✅ | bois d'œuvre…pays des bois | Koad-prenn…argoad | Famille « koad » — complète |
| 70–93 | ✅ | vert…léger, agile | glas…skañv | Adjectifs — complets |

#### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| Famille de mots → extraire | ✅ | Famille « koad » entièrement extraite |
| Noms collectifs → extraire | ✅ | Arbres et plantes extractés sans articles (collectifs) |
| Nettoyage parenthèses | ✅ | `(rameau)` supprimé de `bleñchenn` |

#### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐ |

#### Problèmes
- 🟡 2 within-page duplicates: `koadour`/`bûcheron` (lines 4 & 60), `koadek`/`boisé` (lines 66 & 82) — from GERIADUR and FAMILLE DE MOTS sections

---

### Page 77 (pp. 136–137)

#### Ré-extraction
Paires attendues : ~38 (verb list + grammar examples with `bennak`, `meur a`, `kalz a`)
Paires dans le JSONL : 38

#### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1–14 | ✅ | bouillir…fondre | birvi…teuzi | Verbes mutables — fidèles |
| 15–21 | ✅ | saler…lécher | sal'a…lipat | Verbes non mutables — corrects |
| 22–23 | ✅ | avoir soif, avoir faim | kaout sec'hed, kaout naon | Expressions — correctes |
| 24 | ✅ | se désaltérer | terri ar sec'hed | Correct |
| 25 | ⚠️ | ap. la faim | terri an naon | Abréviation `ap.` non développée — le texte imprimé montre `ap. la faim` |
| 26–27 | ✅ | se nourrir, nourrir | en em vaga, maga | Exemples conjugaison pronominale — valides |
| 28–38 | ✅ | quelqu'un…beaucoup d'étoffe | unan bennak…kalz a zanvez | Exemples grammaire — paires bilingues fidèles à l'image |

#### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| Conjugaison sans traduction → exclure | ✅ | Table pronominale exclue |
| Exercices monolingues → exclure | ✅ | Exercice p136 ignoré |
| Errata `kalz a dud a vary` → `kalz a dud a varv` | ✅ | Correctement appliqué (ligne 37) |
| Exemples bilingues dans grammaire → extraire | ✅ | Exemples `bennak`, `meur a`, `kalz a` extraits |

#### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐⭐ |

#### Problèmes
- 🟡 `ap. la faim` — abbreviation residual (line 25)

## Prompt Assessment

The extraction prompt and book-specific prompt together provide excellent coverage for this textbook. Key observations:

1. **Section exclusion rules are well-defined** — DISPLEGADUR, YEZADUR, EXERCICES, SKRIVANENN, MUNUTENNOU sections are properly excluded across all reviewed pages.

2. **GERIADUR extraction works very well** — The detailed instructions for vocabulary lists with articles, mutations, and grammatical markers produce clean, high-quality pairs.

3. **Famille de mots handling is correct** — Derived words are properly extracted as individual pairs.

4. **Errata table is properly applied** — The correction on p137 (`kalz a dud a vary` → `kalz a dud a varv`) was correctly applied.

5. **Potential addition for book prompt** — A deduplication rule for within-page repeats could be beneficial. Words that appear in both the GERIADUR and FAMILLE DE MOTS sections on the same page get extracted twice. Consider adding: *"Si un mot apparaît dans le GERIADUR et dans la FAMILLE DE MOTS de la même page, ne l'extraire qu'une seule fois."*

6. **The `composit.` case on p12** — The image genuinely shows `composit.` as the printed text (abbreviation for "composition"). The current rules say to clean abbreviations like `m.`, `f.`, `adj.`, but `composit.` is not a grammatical abbreviation — it's a word abbreviation that is faithful to the source text. This is acceptable behavior.

## Final Verdict

| Category | Rating |
|----------|--------|
| Accuracy | ⭐⭐⭐⭐⭐ |
| Completeness | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐½ |
| Prompt compliance | ⭐⭐⭐⭐⭐ |
| Data integrity | ⭐⭐⭐⭐ |
| **Overall** | **⭐⭐⭐⭐½** |

### Required Actions
1. **Fix abbreviation residual** — p77 line 25: decide whether `ap. la faim` should be expanded or the pair should be dropped (the source text is itself abbreviated)
2. **Deduplicate within-page pairs** — 8 duplicate pairs across 6 files should be deduplicated (post-processing or prompt rule)
