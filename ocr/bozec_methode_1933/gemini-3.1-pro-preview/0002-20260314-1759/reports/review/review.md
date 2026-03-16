# Quality Review — bozec_methode_1933

> **Run**: `0002-20260314-1759`
> **Model**: `gemini-3.1-pro-preview`
> **Reviewer**: Antigravity (LLM-as-Judge)
> **Date**: 2026-03-15
> **Pages reviewed**: 5 / 51 (strategy: lowest + highest + flagged + random)
> **Corpus**: 1396 pairs (1344 unique) across 51 JSONL files

## Corpus Stats

| Metric | Value |
|--------|-------|
| Total pairs (raw) | 1396 |
| Unique pairs | 1344 |
| Cross-page duplicates | 38 |
| Malformed JSON lines | 0 |
| Short entries (≤2 chars) | 6 |
| Abbreviation residuals | 0 |
| Unresolved em-dashes | 0 |
| False Impossible pages | 0 |

**Notes on corpus stats**:
- The extraction report header states "1267 pairs" and "46 / 51 pages", but the actual `extracted/` folder contains **51 JSONL files** with **1396 raw pairs**. The report table only lists 46 rows (pages 11, 17, 30, 41, 50 are missing from the report table despite having JSONL files). This is a bookkeeping discrepancy in the report generator, not an extraction issue — all 51 pages were in fact processed.
- All 6 short entries are legitimate Breton words: `ki` (chien), `du` (noir), `re` (trop), `ya` (oui), `ed` (blé).
- The 38 cross-page duplicates are expected: this is a textbook where vocabulary words recur across lessons (e.g., `mamm`/`mère` appears in lessons on pages 05, 11, 25).

## Page Verdicts

| Page | Pairs | Accuracy | Completeness | Issues |
|------|-------|----------|--------------|--------|
| p71 | 3 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | — |
| p74 | 71 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 1 missing pair (pal, ranv split) |
| p25 | 40 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Devoir section questionably included |
| p30 | 46 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | — |
| p44 | 9 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | — |

## Issues

### 🔴 Critical
None

### 🟡 Warning

1. **Extraction report count mismatch**: The auto-generated `report.md` states 46 pages / 1267 pairs, but `extracted/` contains 51 JSONL files / 1396 pairs. Five pages (11, 17, 30, 41, 50) are missing from the report table. This is a report-generator bookkeeping bug, not an extraction failure.

2. **p25 — Devoir sentences included**: On page 25 (pp. 44–45), the `Devoir` section at the bottom contains Élocution-style sentences (e.g., "Moereb an dimezell a zo pinvidik" / "La tante de la demoiselle est riche"). These are extracted as bilingual pairs (lines 33–40 of the JSONL). The book-prompt says "Devoir / Devoir écrit → exclude" but these specific sentences are genuinely bilingual vis-à-vis pairs (breton left, french right), unlike fill-in-the-blank exercises. This is a **borderline case** — the extraction chose to include them because they are complete, aligned bilingual sentences. However, the `Dever.` / `Devoir.` title itself (line 33) should arguably not be extracted as a bilingual pair.

3. **p74 — "pal, ranv" split**: The image shows `pal, ranv f.` → `pelle, bêche` as a single line. The extraction split this into two separate pairs: `pal` / `pelle` and `ranv` / `bêche`. This is actually the correct behavior per prompt rules (split enumerations), but the image arguably shows a single vocabulary entry. Minor — either interpretation is acceptable.

### 🟢 Info

1. **p71 — Correct exclusion of pronoun table**: Page 71 (pp. 136–137) contains a full "Raganoiou damziskoueza / Pronoms indéfinis" table. This was correctly excluded per the book prompt rule: "Tableaux de pronoms, déterminants et mots grammaticaux → exclure entièrement". Only the two image captions and the section title were extracted (3 pairs total). This is **exemplary** prompt compliance.

2. **p30 — Correct exclusion of THÈME section**: The right-side page contains a full THÈME exercise. Correctly excluded.

3. **p44 — Excellent strophe-level segmentation for Lennadenn**: The prose poem "Maro ar bleiz" / "La mort du loup" is segmented by logical paragraph/strophe boundaries as required by the exception rule. BRIZEUX attribution correctly excluded.

4. **Cross-page duplicates are pedagogically expected**: The 38 duplicates (2.7% of total) are recurring vocabulary across successive lessons — entirely normal for a textbook.

## Tricky Page Deep Reviews

### === REVIEW ===

## Page 71 (pp. 136–137)

### Ré-extraction
Paires attendues : 3
Paires dans le JSONL : 3

### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1 | ✅ | Personne ne se repose, chacun a son travail ; tous se hâtent. | Den ebet ne ziskuiz ; pep hini en deus e labour ; holl e hastont. | Légende d'illustration, conforme |
| 2 | ✅ | PRONOMS INDÉFINIS | RAGANOIOU DAMZISKOUEZA | Titre de section, conforme |
| 3 | ✅ | Cueillette des pommes : les uns et les autres s'entr'aident. | Kutuilhadeg avalou : an eil re hag ar re all en em sikour. | Légende d'illustration, conforme |

### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| Tableaux de pronoms/déterminants exclus | ✅ | Toute la section "Raganoiou damziskoueza" excluse |
| Devoir exclu | ✅ | Les deux sections Devoir (breton et français) exclues |
| Espaces syllabiques | N/A | Aucun sur cette page |
| Tirets cadratins | ✅ | Tirets de la section Devoir non extraits (section exclue) |

### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐⭐ |

### Problèmes
- Aucun

### === /REVIEW ===

---

### === REVIEW ===

## Page 74 (pp. 142–143)

### Ré-extraction
Paires attendues : ~72 (2 titles + 70 vocabulary words)
Paires dans le JSONL : 71

### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1 | ✅ | L'agriculture | Al labour-douar | Titre de leçon, conforme |
| 2 | ✅ | Noms | Anoiou | Titre de section, conforme |
| 3-24 | ✅ | blé, sarrazin, froment, seigle, avoine, orge, lin, chanvre, foin, paille, cuscute, chèvre-feuille, gui, lichen, mousse, chiendent, liseron, semence, épis, balles, javelle, gerbe | ed, ed-du, gwiniz, segal, kerc'h, heiz, lin, kanab, foenn, plouz, bleo ar Werc'hez, gwezvoud, uhel-var, kinvi, man, treuzgeot, troell, had, toc'had, pell, dramm, feskenn | Vocabulaire page gauche — toutes les marques de genre (c., m., f.) correctement supprimées |
| 25-46 | ✅ | lien, moisson, litière, fumier, ... auge | ere, eost, gouzer, teil, ... laouer | Vocabulaire page gauche (suite) — conforme |
| 47-58 | ✅ | échelle, outil, marteau, ... fourche | skeul, benveg, morzol, ... forc'h | Vocabulaire page droite — conforme |
| 59 | ✅ | pelle | pal | Correct (pal, ranv split en deux paires) |
| 60 | ✅ | bêche | ranv | Correct (suite du split) |
| 61-71 | ✅ | houe, herse, rouleau, semoir, moissonneuse, hache-paille, courroie, chaîne, charrette/voiture, essieu, brouette | pigell, oged, ruilhenn, haderez, mederez, drailherez, lerenn, chadenn, karr, ahel, karrigell | Vocabulaire page droite — conforme |

### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| Marques de genre supprimées | ✅ | Tous les `c.`, `m.`, `f.` supprimés |
| Variantes entre parenthèses supprimées | ✅ | `(kolo)`, `(touskan)`, `(treskaou)`, `(bilvieu)`, `(tranch m.)`, `(yenn)`, `(ervenn)` tous supprimés |
| THÈME exclu | ✅ | Section THÈME sur page droite exclue |
| Énumérations éclatées | ✅ | "terreau, marne" etc. conservés comme une seule entrée car c'est un seul champ français |

### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐⭐ |

### Problèmes
- 🟢 Completeness: approximately 1 borderline pair could be argued as missing (the title line "Al labour-douar -- L'agriculture" has the `--` separator which is correctly handled, but the extraction renders it as a standalone title without the "NOMS — ANOIOU" section title from the left page which was provided separately on line 2)

### === /REVIEW ===

---

### === REVIEW ===

## Page 25 (pp. 44–45)

### Ré-extraction
Paires attendues : ~33 (excluding Devoir) or ~40 (including Devoir sentences)
Paires dans le JSONL : 40

### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1 | ✅ | Grammaire | Yezadur | Titre, conforme |
| 2-11 | ✅ | Parler, je parle, être, je suis, écrire, regarder, j'ai, il a, grandir, bâtir | Komz, me a gomz, beza, me a zo, skriva, sellout, am eus, en deus, brasaat, sevel | Verbes section 1 — conformes |
| 12-20 | ✅ | Père, mère, garçon, chien, poissons, arbres, pierres, maisons, chemins | Tad, mamm, paotr, ki, pesked, gwez, mein, tier, hentchou | Noms section 2 — conformes |
| 21-32 | ✅ | Petit, grand, longue, courte, riche, pauvre, blanc, noir, haut, bas, chaud, froid | Bihan, bras, hir, berr, pinvidik, paour, gwenn, du, uhel, izel, tomm, yen | Adjectifs section 4 — conformes |
| 33 | ⚠️ | Devoir. | Dever. | Le titre "Dever./Devoir." est extrait comme paire — discutable |
| 34-40 | ⚠️ | La tante de la demoiselle est riche. / J'ai une petite filleule. / ... | Moereb an dimezell a zo pinvidik / Eur filhorez vihan am eus. / ... | Section Devoir — ce sont des phrases bilingues complètes vis-à-vis, mais la section est titrée "Devoir" |

### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| Exclusion section Devoir | ⚠️ | Les sentences du Devoir de la page 25 sont de vraies paires bilingues vis-à-vis, pas des exercices à trous. L'extraction les a incluses — interprétation borderline |
| Section articles (3.) exclue | ✅ | La section "Un, une, des... sont des articles" exclue (mots-outils) |
| Section "Klaskit ha skrivit" exclue | ✅ | Consigne pédagogique exclue |
| Espaces syllabiques | N/A | Aucun détecté |

### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐⭐ |

### Problèmes
- 🟡 Le titre "Dever."/"Devoir." ne devrait pas être extrait comme paire — il s'agit d'une étiquette de section, pas d'un contenu bilingue
- 🟢 Les phrases du Devoir sont de vraies paires bilingues en vis-à-vis — l'inclusion est défendable

### === /REVIEW ===

---

### === REVIEW ===

## Page 30 (pp. 54–55)

### Ré-extraction
Paires attendues : ~46
Paires dans le JSONL : 46

### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1 | ✅ | Les animaux domestiques | Loened an ti | Titre, conforme |
| 2 | ✅ | Noms | Anoiou | Titre section, conforme |
| 3-26 | ✅ | le cheval, les chevaux, la pouliche, l'âne, le bœuf, la vache, la génisse, la chienne, la chatte, la chèvre, les chevreaux, le mouton, la brebis, le bouc, la poule, le pigeon, l'abeille, l'aiguillon, la crinière, les cornes, la queue, la sueur, le crin, un œuf | ar marc'h, ar c'hezek, an ebeulez, an azen, an ejen, ar vioc'h, an ounner, ar giez, ar gazez, ar c'havr, ar menned, an danvad, an danvadez, ar bouc'h, ar yar, ar goulm, ar wenanenn, ar flemm, ar moue, ar c'herniou, al lost, ar c'houezenn, ar reun, eur vi | Vocabulaire animaux — conforme. Marques parenthèses (annouar), (c'haor) correctement supprimées |
| 27 | ✅ | Verbes | Verbou | Titre section, conforme |
| 28-37 | ✅ | hurler, mugir, hennir, sauter, gambader, miauler, roucouler, glousser, en becquetant, à paître | yudal, blejal, c'houirinat, sailha, tripal, miaoual, grougousat, sklokal, en eur bigosat, o peuri | Verbes — conformes. "en eur bigosat"/"en becquetant" et "o peuri"/"à paître" sont des formes verbales OK |
| 38 | ✅ | Adjectifs | Anoïou gwan | Titre section, conforme |
| 39-46 | ✅ | alezane, tachetée, fin, hardi, trempée de, semblable, libre, méchant | baian, briz, munut, hardis, gleb-dour-teil gant, henvel, dishual, drouk | Adjectifs — conformes |

### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| THÈME exclu | ✅ | Section THÈME page droite exclue |
| Marques de genre/parenthèses | ✅ | `(annouar)`, `(c'haor)`, `(u)` supprimés |
| Légendes d'illustrations | N/A | Les illustrations sont sans légendes textuelles distinctes |
| Verbou = liste de vocabulaire → inclus | ✅ | Pas de paradigme ici, juste une liste → correctement inclus |

### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐⭐ |

### Problèmes
- Aucun

### === /REVIEW ===

---

### === REVIEW ===

## Page 44 (pp. 82–83)

### Ré-extraction
Paires attendues : 9 (title + subtitle + 7 strophes)
Paires dans le JSONL : 9

### Comparaison détaillée

| # | Statut | Français (JSONL) | Breton (JSONL) | Observation |
|---|--------|------------------|----------------|-------------|
| 1 | ✅ | HUITIÈME LECTURE | EIZVET LENNADENN | Titre, conforme |
| 2 | ✅ | La mort du loup | Maro ar bleiz | Sous-titre, conforme |
| 3 | ✅ | L'été, lorsque du ciel tombe enfin la nuit fraîche, Les bestiaux, tout le jour retenus dans la crèche, Vont errer librement, au pied des verts coteaux. | En hanv, pa ziskenn erfin an noz gant he freskadurez, ar chatal, dalc'het epad an deiz er c'hreier, a vez loskaet en o frankiz. | Strophe 1 — conforme |
| 4 | ✅ | Ils suivent pas à pas les longs détours des eaux, S'étendent sur les prés, où, dans la vapeur brune, Hennissent bruyamment aux rayons de la lune. | A-hed ar runiou glas, e heuilhont, kammed ha kammed, kammigellou hir ar gwaziou, e c'hourvezont war ar leton, pe e c'houirinont gant safar, e morenn an noz, ouz sklaerijenn al loar. | Strophe 2 — conforme |
| 5-9 | ✅ | (remaining strophes) | (remaining strophes) | Strophes 3–7 — conformes, segmentation par unité narrative |

### Vérification des règles livre

| Règle | Statut | Détail |
|-------|--------|--------|
| Strophes non éclatées en phrases | ✅ | Chaque paragraphe breton = une strophe = un segment |
| Numérotation supprimée | N/A | Cette lecture n'est pas numérotée par strophes (texte continu), segmenté par paragraphes logiques |
| Attribution d'auteur exclue | ✅ | "BRIZEUX." en fin de page droite exclu |
| Titre section exclu | ✅ | N/A — les titres sont bilingues, donc extraits |

### Scores page

| Dimension | Note |
|-----------|------|
| Précision | ⭐⭐⭐⭐⭐ |
| Complétude | ⭐⭐⭐⭐⭐ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Conformité au prompt | ⭐⭐⭐⭐⭐ |
| Intégrité | ⭐⭐⭐⭐⭐ |

### Problèmes
- Aucun

### === /REVIEW ===

## Prompt Assessment

The extraction prompt (`prompts/bozec_methode_1933.md`) and the global prompt are both well-crafted and comprehensive. The extraction demonstrates excellent compliance across all reviewed pages.

**Strengths**:
- The strophe-level exception for Lennadennou is correctly implemented (p44)
- Pronoun/determiner table exclusion is correctly applied (p71)
- Gender markers, pronunciation hints, and variant parentheticals are consistently cleaned
- THÈME sections systematically excluded across all vocabulary pages
- Syllabic spaces appear to be correctly rejoined throughout the corpus (no residuals detected)

**Potential prompt refinements**:
1. **Devoir section ambiguity**: The current rule says "Devoir / Devoir écrit → exclure" but some Devoir sections (e.g. p25) contain genuine bilingual vis-à-vis sentences, not fill-in-the-blank exercises. The rule could be refined to distinguish between:
   - Exercise-type Devoirs (fill-in-the-blank, monolingue) → exclude
   - Vis-à-vis sentence Devoirs (complete bilingual sentences) → include
2. **Section title extraction**: Titles like "Dever."/"Devoir.", "Verbou"/"Verbes", "Anoiou"/"Noms" are currently extracted as bilingual pairs. While these are technically bilingual, they add limited value to the corpus. A rule to exclude pure section headers could be considered.

## Final Verdict

| Category | Rating |
|----------|--------|
| Accuracy | ⭐⭐⭐⭐⭐ |
| Completeness | ⭐⭐⭐⭐½ |
| Normalisation | ⭐⭐⭐⭐⭐ |
| Prompt compliance | ⭐⭐⭐⭐½ |
| Data integrity | ⭐⭐⭐⭐⭐ |
| **Overall** | **⭐⭐⭐⭐½** |

### Required Actions
1. **Fix report-generator bookkeeping**: 5 pages are missing from the extraction report despite having corresponding JSONL files (report says 46/51 but 51/51 were processed). This is a code bug, not an extraction issue.
2. **Consider clarifying Devoir rule**: Distinguish exercise-type Devoirs from vis-à-vis sentence Devoirs in the book prompt.
3. **Consider excluding section titles**: "Verbou"/"Verbes", "Anoiou"/"Noms", "Dever."/"Devoir." as standalone pairs add noise.
