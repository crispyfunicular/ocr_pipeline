# Instructions spécifiques : Yez Hor Tadou – Cours de breton (1940)

## Nature de l'ouvrage

Cet ouvrage est un **cours de breton** de 1940. Il contient :

1. **Leçons grammaticales** avec explications en français et exemples bilingues
2. **Tableaux de vocabulaire** avec paires breton ↔ français
3. **Exercices** de traduction et à trous
4. **Textes de lecture** (« Pennad da Studia ») en breton

### Disposition

Les pages sont en vis-à-vis. Le contenu mélange français et breton au sein de chaque page (les pages ne sont PAS en opposition bilingue gauche/droite). Les paires sont à trouver dans les listes de vocabulaire, les exemples et les exercices de traduction.

---

## Règles d'extraction

> **RÈGLE CRITIQUE : Seuls les mots ou segments bretons ayant une traduction française explicite en vis-à-vis doivent être pris en compte ; TOUT le reste doit être strictement ignoré.** Ne tentez pas d'extraire des colonnes de pluriels, de variantes mutées, de formes de conjugaison ou des mots isolés qui n'ont pas de traduction française directe en face.

### Vocabulaire

Quand des mots sont présentés en paires breton ↔ français (en colonnes ou en listes), extrayez chaque paire :
```json
{"breton": "Ti", "français": "Maison"}
{"breton": "Taol", "français": "Table"}
{"breton": "Kador", "français": "Chaise"}
```

### Vocabulaire « GERIADUR »

Les sections intitulées **GERIADUR** présentent des listes de mots avec articles, mutations et formes plurielles. Elles sont structurées en deux colonnes (breton à gauche, français à droite). Extrayez chaque paire :
```json
{"breton": "ur baner", "français": "un drapeau"}
{"breton": "ar vaner", "français": "le drapeau"}
{"breton": "baneriou", "français": "des drapeaux"}
{"breton": "ar baneriou", "français": "les drapeaux"}
```

> Les articles (`un/ur`, `le/ar`, `la/al`) font partie du syntagme — conservez-les dans le champ breton ET français.

### Famille de mots (« FAMILLE DE MOTS » / « GERIADENN »)

Ces sections regroupent des mots dérivés d'une même racine bretonne avec leur traduction française. Extrayez chaque paire :
```json
{"breton": "skol", "français": "école"}
{"breton": "skolaer", "français": "instituteur"}
{"breton": "skolaerez", "français": "institutrice"}
{"breton": "skolveurieg", "français": "pédagogique"}
```

### Exemples bilingues dans le texte grammatical

Les explications grammaticales contiennent des exemples bilingues intégrés, souvent après `Ex. :` ou entre tirets. Extrayez **uniquement** les paires clairement bilingues — chaque champ doit contenir **une seule langue** :
```json
{"breton": "hor c'halon", "français": "notre cœur"}
{"breton": "ho mamm", "français": "votre mère"}
```

> **Ne mélangez jamais** les deux langues dans un même champ. Si un exemple contient `Kalon, cœur ; hor c'halon, notre cœur`, extrayez uniquement la paire breton/français propre (`hor c'halon` / `notre cœur`), pas le mélange.

> **Attention** : ne fabriquez pas de paires à partir d'exemples purement grammaticaux (déclinaisons, mutations). Les exemples doivent présenter un mot/phrase breton et sa traduction française.

### Tableaux de conjugaison bilingues

Certaines leçons contiennent des tableaux de conjugaison avec les formes bretonnes et françaises en regard. Quand les deux colonnes sont présentes, extrayez chaque ligne :
```json
{"breton": "Me a gar", "français": "J'aime"}
{"breton": "Te a gar", "français": "Tu aimes"}
{"breton": "Eñ a gar", "français": "Il aime"}
```

> Si le tableau ne montre que la conjugaison bretonne sans traduction française → **exclure**.

### Sections à exclure

- **Exercices à trous** (phrases avec `...`, `___`, mots tronqués) → **exclure** — ce ne sont pas des traductions complètes
- **Exercices de traduction monolingue** (« Traduisez en breton : ... ») sans réponse fournie → **exclure**
- **Textes « Pennad da Studia »** = textes de lecture monolingues bretons → **exclure**
- **Tableaux de conjugaison** sans traduction française → **exclure**
- **Remarques grammaticales** en prose → **exclure**
- **Titres de section bilingues** (ex : "DISPLEGADUR - VERB (Conjugaison)", "YEZADUR (Grammaire)") → **exclure**
- **SKRIVANENN** (dictées/exercices d'écriture) → **exclure** — exercices monolingues bretons
- **MUNUTENNOU HIR / MUNUTENN** = textes longs monolingues (histoires, récits) → **exclure** entièrement
- **EXERCICES / POELLADENNOU** = exercices de traduction monolingues (« Lakait e galleg » = « Mettez en français », « Lakait e brezhoneg » = « Mettez en breton ») sans réponse fournie → **exclure**

### Phrases avec traductions intercalées entre parenthèses

Les phrases où une traduction apparaît entre parenthèses à l'intérieur d'une autre langue (ex : « Douaret am eus (j'ai butté) ma betrabez ») ne constituent PAS des paires propres → **exclure**.

### Errata

L'ouvrage contient une liste d'errata (page 02). Lorsque vous traitez une page concernée, **appliquez la correction** indiquée ci-dessous — utilisez la forme corrigée (colonne « lire ») à la place de la forme erronée (colonne « au lieu de ») :

| Au lieu de | Page | Lire |
|---|---|---|
| Va fenn | 59 | va fenn |
| Her c'hoan | 66 | her c'hoan |
| eun iter | 67 | eun ister |
| O c'houzout | 67 | o c'houzout |
| as oabl | 75 | an oabl |
| a wreg | 60 | e wreg |
| an anzer | 76 | an amzer |
| daour | 76 | douar |
| a youc'he | 77 | a youe'he |
| muattion | 81 | mutation |
| trochet | 83 | troc'het |
| maintinvez | 87 | mintinvez |
| diouz ra mintin | 87 | diouz ar mintin |
| berr as deiz | 89 | berr an deiz |
| eur c'hard eur | 91 | eur c'hard eur |
| mil var | 91 | mil vad |
| pa c'hello : | 91 | pa c'hello |
| e skoas eun taol | 93 | a skoas eun taol |
| buhan | 99 | buan |
| run et sioujod | 106 | run e sioujod |
| kalz a dud a vary | 137 | kalz a dud a varv |
| n'oa ket brao henvel | 141 | n'oa ket brao envel |
| ce ont lâ | 49 | ce sont lâ |

> Dans les lettres d'approbation de N.N. S.S. les Évêques :
> - « la nuance » → « les nuances »
> - « patriotisme » → « patrimoine »

> Ajouter page 158, colonne du milieu, avant « eun. am... » : « se fent après : »

### Qualité du scan

Les pages sont nettes et lisibles. Le corps du texte est de taille standard.
