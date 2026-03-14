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
{"breton": "Asamblez", "français": "ensemble, en même temps"}
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

### Exemples traduits au sein des définitions

Certaines entrées contiennent des exemples d'usage ou des expressions complètes avec leur traduction (parfois introduits par `Ex. :`, `par ex. :`, ou directement intégrés dans le texte de la définition). Si le texte contient un segment (phrase ou expression) breton explicitement accompagné de sa traduction française au sein de la définition, extrayez-le comme une paire bilingue **séparée**. 
> Exemple tiré de l'entrée *Gwener* : `Da Vener ar Groaz, le Vendredi-Saint` → `{"breton": "Da Vener ar Groaz", "français": "le Vendredi-Saint"}`
> Exemple tiré de l'entrée *Gwener* : `Disul e oa ar pardon, le pardon avait lieu dimanche` → `{"breton": "Disul e oa ar pardon", "français": "le pardon avait lieu dimanche"}`
> Exemple tiré de l'entrée *Gwener* : `disul ha disul all a vezo oferen vintin, dimanche prochain et dimanche en-huit, il y aura messe basse, première messe.` → `{"breton": "Disul ha disul all a vezo oferen vintin", "français": "dimanche prochain et dimanche en-huit, il y aura messe basse, première messe."}`
Si l'exemple est monolingue sans traduction claire associée, **ignorez-le**.

### Superlatifs et comparatifs

Quand un mot est défini comme un superlatif d'un adjectif (`adj. superl. de [adjectif de base], [traduction]`), **vous devez extraire DEUX paires distinctes** :
1. Une paire pour l'adjectif de base avec sa traduction littérale.
2. Une paire pour la forme superlative, en ajoutant « **le plus** » devant l'adjectif français.

> Exemple : `Danjerusa, adj. superl. de danjeruz, dangereux` → doit générer DEUX lignes :
> `{"breton": "Danjeruz", "français": "dangereux"}`
> `{"breton": "Danjerusa", "français": "le plus dangereux"}`

> Exemple : `Brasa, adj. au superl., le plus grand. Braz, grand` → doit générer DEUX lignes :
> `{"breton": "Braz", "français": "grand"}`
> `{"breton": "Brasa", "français": "le plus grand"}`

**Même règle pour les comparatifs** (`compar. de X`, `adj. compar.`) : extraire le comparatif ET l'adjectif de base en deux paires distinctes. Le comparatif français utilise « **plus** » (sans article) devant l'adjectif.

> Exemple : `Huelloc'h, adj. compar. de huel, haut, élevé` → doit générer DEUX lignes :
> `{"breton": "Huel", "français": "haut, élevé"}`
> `{"breton": "Huelloc'h", "français": "plus haut, plus élevé"}`
>
> Exemple : `Muioc'h, adv. compar. de kalz, beaucoup` → doit générer DEUX lignes :
> `{"breton": "Kalz", "français": "beaucoup"}`
> `{"breton": "Muioc'h", "français": "plus, davantage"}`

### Définitions longues et encyclopédiques

Certaines entrées ont des définitions étendues avec explications grammaticales ou phonétiques. **Gardez uniquement la première traduction concise**, pas les explications :

Par exemple pour `Andurer, ind. pr., 3° p. s. impers. de anduri, endurer, souffrir. Ce mot est français...` :
```json
{"breton": "Andurer", "français": "endurer, souffrir"}
```

### Traductions tronquées en fin de page

Les entrées situées tout en bas de la page droite ont parfois leur traduction coupée.
> Exemple : `Ziskar, ind. pr., 3e p. s., et inf. pr., 1 M. de diskar, abat-` 
Si la traduction française est manifestement inachevée (ici "abat-" coupé par la fin de page), **IGNOREZ entièrement la ligne**. Ne tentez pas de deviner ou de compléter le mot manquant ("abattre"). La paire doit être extraite telle qu'elle est imprimée, uniquement si elle est complète.

### Formes fléchies et conjuguées

Certaines entrées présentent des formes verbales fléchies (conjuguées) qui ne sont traduites que par un verbe à l'infinitif en français. **Vous devez ignorer ces formes fléchies car elles ne constituent pas une paire de traduction exacte.**

Cela se présente sous deux formes principales :

**Les entrées groupées :** Plusieurs formes verbales (nom verbal, participe passé, formes conjuguées) sont regroupées sous une seule traduction à l'infinitif.  
- Exemple : `Pardon, Pardonêt, Pardoni, Pardonit, Pardono, Pardonomp...  pardonner` → **IGNOREZ** toute la ligne.  

**Les entrées individuelles avec indications grammaticales :** L'entrée commence par le mot breton suivi de marques de personne, de nombre, de temps et de mode (ex: `ind. pr., 3e p. s.`, `fut. simp.`, `1re p. pl.`, `1 M. de...`), mais la traduction française n'est qu'un infinitif.

- Exemple : `- Zell, ind. pr., 3e p. s., 1 M. de sellat, regarder.` → **IGNOREZ** cette ligne car "Zell" (qui signifie "il/elle regarde", 3ème personne du singulier) est traduit à tort par l'infinitif "regarder".  
- Exemple : `Zesk, ind. pr., 3e p. s., 1 M. de deski, apprendre, enseigner ; — zeski.` → **IGNOREZ** cette ligne pour la même raison.  
- Exemple : `Oue, pas. déf., 3e p s. de beza, être.` (Traduit par "être" au lieu de "fut") → **IGNOREZ**  
- Exemple : `Oump, ind. pr., 1re p. pl. de beza, être.` (Traduit par "être" au lieu de "sommes") → **IGNOREZ**  
- Exemple : `Ordren, inf. pr. et 3e p. s., ind. pr., ordonner.` → La traduction donnée est l'infinitif "ordonner", mais le mot breton `Ordren` peut être une 3e personne ("il ordonne"). S'il y a une ambiguïté forme conjuguée / traduction à l'infinitif, **rejetez la paire**.  

Si la forme fléchie est traduite par la forme fléchie correspondante en français, vous pouvez l'extraire (ex: un participe passé traduit par un participe passé). Mais si la traduction française donne juste l'infinitif pour une forme conjuguée bretonne, **ignorez-la**.

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
