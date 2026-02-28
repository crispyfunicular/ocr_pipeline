# Instructions spécifiques : Normant – Lexique breton-français (1902)

## Nature de l'ouvrage

Cet ouvrage est un **dictionnaire breton-français** de 1902. Il contient :

- Des pages préliminaires de **notions grammaticales** (« NOTIONS PRÉLIMINAIRES ») avec règles de mutation, d'article et de pronoms possessifs — ces pages contiennent des exemples bilingues exploitables
- Des pages de **conjugaison de verbes** avec tableaux breton/français en regard (KAOUT/avoir, BEZA/être, etc.)
- Un **dictionnaire principal** en deux colonnes avec des entrées de A à Z

### Direction de traduction

> **ATTENTION** : le mot-vedette (en gras) est en **breton**, la traduction/définition est en **français**. C'est l'inverse du `geriadur_lexique_1927` — veillez à bien affecter chaque langue au bon champ JSONL.

---

## Règles d'extraction

### Entrées du dictionnaire

Chaque entrée a le format :
```
Mot-vedette breton, info grammaticale, traduction/définition française.
```

Extrayez le mot-vedette breton et la traduction française en supprimant toute information grammaticale :

```json
{"breton": "Anaout", "français": "connaître"}
{"breton": "Anat", "français": "connu, clair, évident"}
{"breton": "Arc'hant", "français": "argent"}
{"breton": "Artikl", "français": "article"}
{"breton": "Asamblež", "français": "ensemble, en même temps"}
```

### Abréviations grammaticales à supprimer

Supprimez de la sortie toutes les abréviations grammaticales :
- `inf. pr.` (infinitif présent), `ind. pr.` (indicatif présent), `p. p.` (passé participe)
- `3° p. s.` (3e personne du singulier), `m. s.` (masculin singulier), `f. s.` (féminin singulier)
- `adj.`, `adv.`, `prép.`, `conj.`
- `Pl.` (pluriel) — supprimez la mention et le mot pluriel sauf s'il constitue une entrée indépendante

### Notes étymologiques

Les commentaires étymologiques comme « C'est le mot latin », « C'est le mot français », « Ce mot est français » doivent être **supprimés** de la traduction. Gardez uniquement la traduction utile.

### Renvois et références croisées

- Les entrées qui ne contiennent qu'un renvoi (`Voir...`, `P. p. de...`, `S.`) sans traduction propre → **ignorer**
- Les entrées avec `P. p.` (passé participe de...) → **ignorer** si elles ne donnent pas de traduction
- Les entrées `pass. déf.` ou `p. p.` qui pointent vers un autre mot sans traduction → **ignorer**
- Les entrées « Voir précéd. » ou « Voir ce mot » sans traduction propre → **ignorer**

### Exemples intégrés (`Ex. :`)

Certaines entrées contiennent des exemples d'usage marqués par `Ex. :`. Si l'exemple contient une phrase avec sa traduction dans l'autre langue, extrayez-le comme paire séparée. Si l'exemple est monolingue, **ignorez-le**.

### Définitions longues et encyclopédiques

Certaines entrées ont des définitions étendues avec explications grammaticales ou phonétiques. **Gardez uniquement la première traduction concise**, pas les explications :

Par exemple pour `Andurer, ind. pr., 3° p. s. impers. de anduri, endurer, souffrir. Ce mot est français...` :
```json
{"breton": "Andurer", "français": "endurer, souffrir"}
```

### Entrées avec synonymes multiples

Quand une entrée liste plusieurs traductions séparées par des virgules, gardez-les toutes dans le champ français :
```json
{"breton": "Deski", "français": "apprendre, enseigner"}
{"breton": "Gwenn", "français": "blanc, pur"}
```

> **Entrées pronominales groupées** (ex : `Anez-han, Anez-hi, Anez-ho`) : ces entrées mélangent plusieurs formes avec de longues explications grammaticales. Elles sont à **exclure entièrement** — faible valeur, fort risque d'erreur d'alignement.

### Pages de notions préliminaires

Les pages de grammaire contiennent des exemples bilingues intégrés. Extrayez **uniquement** les exemples clairement bilingues (marqués `Ex.` ou en paires dans le texte) :
```json
{"breton": "Kurunen", "français": "couronne"}
{"breton": "Peden", "français": "prière"}
{"breton": "Tra", "français": "chose"}
{"breton": "Gad", "français": "lièvre"}
{"breton": "Bro", "français": "pays"}
```

Les règles elles-mêmes (1re Règle, 2me Règle, etc.) sont des explications monolingues → **exclure**.

### Tableaux de conjugaison

Les pages préliminaires contiennent des **tableaux de conjugaison complète** pour des verbes comme **KAOUT** (avoir) et **BEZA** (être). Chaque ligne du tableau présente un pronom breton, une forme verbale bretonne, et la traduction française en regard :

```json
{"breton": "Em (b)euz", "français": "j'ai"}
{"breton": "E peuz", "français": "tu as"}
{"breton": "En, e deuz", "français": "il, elle a"}
{"breton": "Hor beuz", "français": "nous avons"}
{"breton": "Ho peuz", "français": "vous avez"}
{"breton": "Ho deuz", "français": "ils, elles ont"}
```

> Extrayez **chaque ligne** du tableau comme une paire distincte. Incluez le pronom avec la forme verbale dans le champ breton.
> Les formes entre parenthèses `(b)euz` indiquent une mutation — conservez-les telles quelles.
> N'extrayez les tableaux que si la traduction française est présente en regard.

### Variantes et « Remarque »

Les sections *Remarque* listent des **variantes dialectales** d'un même verbe. Ces variantes ont une valeur limitée pour le corpus car elles représentent des formes inflectées rares. **Ignorez** les listes de variantes dialectales sauf si elles introduisent un **mot autonome** avec une traduction claire.

> Exemple à **ignorer** : `e vefen, e veen, e vén, e vichen, e vijen, e vizen` = variantes dialectales de « je serais » — trop de formes groupées, pas d'unité sémantique propre.

### Entrées multi-sens avec tirets

Certaines entrées ont **plusieurs sens** introduits par un tiret `—`. Extrayez **uniquement** les sens qui constituent une unité sémantique réellement utile (mot + traduction). **Ignorez** :
- Les entrées de **lettres isolées** (A, E, I...) avec des définitions grammaticales (préposition, conjonction, particule) — aucune valeur dans un corpus bilingue
- Les sens purement grammaticaux (particule de liaison, pronom relatif) sans traduction concrete

> Exemple à **ne pas extraire** : `E` = préposition « dans, en » / conjonction « que » / forme de « être » — un seul caractère mappé à des fonctions grammaticales, inutile comme unité sémantique.

### En-têtes de lettre (A, B, C...)

Les en-têtes de section (lettre alphabétique isolée en haut de colonne ou de page) ne sont PAS des entrées → **ignorer**.

### Entrées avec formes plurielles / déclinées

Quand une entrée mentionne le pluriel (ex : `Pl. drouiou`) ou le singulat (ex : `Sing. ebat`), **supprimez** ces formes de la sortie. Gardez uniquement le mot-vedette et sa traduction.

### Qualité du scan

Le texte est en petits caractères mais généralement net et lisible. Les deux colonnes sont bien séparées. Les mots-vedettes en gras sont clairement identifiables.
