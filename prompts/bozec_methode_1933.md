# Instructions spécifiques : Bozec – Méthode de breton (1933)

## Nature de l'ouvrage

Cet ouvrage est une **méthode d'apprentissage du breton** de 1933, organisée en leçons. Chaque leçon s'étale généralement sur deux pages en vis-à-vis :

- **Page de gauche** : leçon en **breton** (vocabulaire, élocution, devoir)
- **Page de droite** : leçon en **français** (mêmes rubriques, même contenu traduit)

> **ATTENTION** : Certaines pages ne sont PAS en vis-à-vis (par ex. pages de grammaire seules, ou pages d'exercices). Dans ce cas, extrayez uniquement les paires bilingues visibles sur la page. Ne tentez PAS de reconstruire la traduction d'une page manquante.

### Structure d'une leçon typique

1. **Illustrations avec légendes bilingues** (en haut) — ex : « Labourerien, al labourerien / des laboureurs, les laboureurs »
2. **Titre de leçon grammaticale** — bilingue (ex : « Anoiou alies (ien, ed, ou) / Noms pluriels (s, x, aux) »)
3. **Section Élocution** — texte continu, breton sur page gauche, français sur page droite
4. **Section Devoir** — exercices écrits, souvent monolingues ou à compléter
5. **Lennadennou / Lectures** — textes en vers ou en prose, numérotés strophe par strophe, alignés page gauche / page droite
6. **Verbou / Verbes** — conjugaisons avec paradigmes
7. **Geriou digemmus / Mots invariables** — vocabulaire en deux colonnes

---

## Règles d'extraction

### Légendes d'illustrations
Les légendes sous les images sont des paires bilingues de haute qualité. Extrayez chaque légende :
```json
{"breton": "Labourerien, al labourerien", "français": "des laboureurs, les laboureurs"}
{"breton": "Pesked, ar pesked", "français": "des poissons, les poissons"}
```

### Titres de leçon
Les titres grammaticaux bilingues doivent être extraits quand les deux langues sont présentes :
```json
{"breton": "Anoiou alies", "français": "Noms pluriels"}
```
> Supprimez les annotations grammaticales entre parenthèses dans les titres (ex : `(ien, ed, ou)`, `(s, x, aux)`, `(diou)`, `(teir)`, `(peder)`).

### Sections Élocution
Ces sections contiennent du texte continu. Le breton est sur la page de gauche, le français sur la page de droite. **Alignez phrase par phrase** en découpant aux points, aux doubles tirets `--`, ainsi qu'aux points d'interrogation (`?`) et d'exclamation (`!`). Les phrases doivent se correspondre dans les deux langues.
> **Note typographique stricte** : Mettez toujours une **espace** avant chaque point d'interrogation (` ?`) et d'exclamation (` !`), tant en breton qu'en français. De plus, chaque point d'interrogation ou d'exclamation doit marquer la fin d'un segment extrait : s'il y a plusieurs questions à la suite, créez autant de paires bilingues.

### Vocabulaire en début de leçon
Certaines leçons listent des mots de vocabulaire en colonnes. Extrayez chaque paire mot par mot :
```json
{"breton": "an tan", "français": "le feu"}
{"breton": "an oabl", "français": "le firmament"}
{"breton": "ar stered", "français": "les étoiles"}
```

### Mots invariables (Geriou digemmus)
Certaines leçons contiennent un tableau de mots invariables en deux colonnes (breton à gauche, français à droite). Extrayez chaque paire :
```json
{"breton": "betek breman", "français": "jusqu'ici"}
{"breton": "ken", "français": "plus"}
{"breton": "ken abret", "français": "si tôt"}
{"breton": "evelhen", "français": "ainsi"}
{"breton": "ivez", "français": "aussi"}
```

### Accumulations de noms
Si le texte présente une longue liste de noms ou d'éléments séparés par des virgules (très fréquent dans les "Exercices d'intuition" ou pour désigner des objets visuels), **divisez cette liste en segments individuels**. Si une phrase d'introduction précède l'énumération (comme "Setu... / Voilà..."), attachez-la au premier élément.
Par exemple, pour : "Setu a hont an daolenn, an nor, ar prenestr" / "Voilà là-bas le tableau, la porte, la fenêtre":
```json
{"breton": "Setu a hont an daolenn,", "français": "Voilà là-bas le tableau,"}
{"breton": "an nor,", "français": "la porte,"}
{"breton": "ar prenestr,", "français": "la fenêtre,"}
```

### Lennadennou / Lectures
Les pages de lecture présentent des textes en vers ou en prose numérotés (1., 2., 3., …), avec le breton à gauche et le français à droite. Extrayez **strophe par strophe** — chaque strophe numérotée constitue un segment. Ne découpez pas ligne par ligne à l'intérieur d'une strophe :
```json
{"breton": "Eun amzer a zo bet, ha ne veze klevet 'N hon touez nemet yez Breiz ; war ar maez, 'vel en kêr, Holl 'komzemp ar yez koz gant hon tadou komzet, En Gwened, en Kerne, Leon ha Landreger.", "français": "Il fut un temps, où l'on n'entendait, parmi nous, que la langue de Breiz : à la campagne comme en ville, nous parlions tous la vieille langue que parlaient nos pères, en Vannes, en Cornouaille, en Léon, en Trégor."}
```

### Sections à exclure

- **Devoir / Devoir écrit** : exercices à compléter, souvent monolingues → **exclure**
- **Notes grammaticales** en bas de page (numérotées `(1)`, `(2)`) : explications de règles → **exclure**
- **Exercices « Skrivet hag echuit ar gerion-man »** (Écrire et compléter les mots suivants) → **exclure** (monolingue, phrases à trous)
- **Sections « Grammaire »** en bas de page droite → **exclure** (consignes monolingues)
- **Sections « Verbou / Verbes »** : paradigmes de conjugaison (1°, 2°, 3°) → **exclure** entièrement (y compris les infinitifs)
- **Tableaux de pronoms ou mots grammaticaux** (ex : *Raganoiou staga* / Pronoms relatifs) → **exclure** (conformément à la règle globale sur les mots-outils)
- **Sections « Thème » / « Da lakat e galleg »** : exercices de traduction dirigés → **exclure** (monolingues ou semi-monolingues)
- **Attributions d'auteur / noms propres** : les lignes de crédit ou signatures d'auteur en fin de texte ou de poème (ex : `JAFFRENNOU (Barzaz-Taldir)`, `MATHALIZ (Breiz divarvel)`, `D'après JAFFRENNOU`) → **exclure**. De façon générale, ne pas extraire les noms propres isolés (noms d'auteurs, de lieux sans traduction, etc.) comme paires bilingues.

### Nettoyage

- **Indications de prononciation** entre parenthèses : `(-ou)`, `(-iou)`, `(-eu)` → supprimer
- **Marques de genre / classe** : `(m)`, `(f)`, `(e)`, `m.`, `f.`, `c.` (avec ou sans parenthèses ou points) → **supprimer du mot breton extrait**. Exemples : `luz c.` → `luz` ; `barr m.` → `barr` ; `treujenn f.` → `treujenn`
- **Formes plurielles ou variantes entre parenthèses** : les mots suivis d'une forme entre parenthèses comme `(deliou)`, `(gwriziou)`, `(skavenn)`, `(skod)` → **supprimer la parenthèse et son contenu**. Exemples : `delienn f. (deliou)` → `delienn` ; `gwrizien f.(gwriziou)` → `gwrizien` ; `skao c. (skavenn)` → `skao`
- Les mots de vocabulaire incluent parfois la mutation après un article : `an oabl (m) (-ou)` → extraire simplement `an oabl`
- **Numérotation de leçon** (ex. `Kentel 3`, `Leçon 3`) → supprimer du contenu extrait, mais extraire le titre de la leçon s'il est bilingue
- **Marques typographiques** : les marques `▶`, `♦`, `•` ou équivalents d'imprimerie ancienne utilisés comme séparateurs → ignorer
- **Tirets cadratins** (`—`, `\u2014`) : ce sont des séparateurs de segments, au même titre que les doubles tirets `--`. Les segments doivent être **découpés** au niveau du tiret cadratin, et celui-ci ne doit **jamais** apparaître dans le corpus extrait.

### Qualité du scan

Les pages sont généralement bien imprimées avec des illustrations claires. La jointure centrale peut légèrement affecter le texte — ignorez uniquement les mots réellement illisibles.
