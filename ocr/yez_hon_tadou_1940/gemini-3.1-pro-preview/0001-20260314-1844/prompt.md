# Extraction de corpus parallèle breton-français

## Objectif

Notre but est de constituer des corpus de segments parallèles bilingues français-breton à partir d'ouvrages de type dictionnaires, lexiques ou manuels d'apprentissage.

Nous cherchons à extraire, quand c'est possible, des **segments** — c'est-à-dire des unités sémantiques (mot, expression, phrase) — ayant une utilité pour créer un corpus bilingue dans le but d'entraîner des modèles à diverses tâches linguistiques, notamment la traduction automatique, mais pas uniquement.

> **RÈGLE FONDAMENTALE : les segments doivent être alignés.** Chaque paire extraite doit correspondre à deux segments qui sont **explicitement en correspondance** sur la page (même ligne, même position dans un tableau, ou en regard l'un de l'autre). N'appariez **jamais** un mot breton avec une traduction française qui n'apparaît pas en regard sur la page. Si un segment n'a pas de correspondant clair et vérifiable visuellement, ignorez-le.

## Instruction critique : fidélité absolue

> **INSTRUCTION CRITIQUE : Ne devinez et n'inventez AUCUN caractère.** Si une lettre ou un mot *individuel* est trop flou pour être lu avec certitude, ignorez ce mot ou cette phrase. **La précision est strictement plus importante que l'exhaustivité.**

> **MAIS : ne rejetez PAS une page entière sous prétexte de « flou général ».** Si le texte imprimé est globalement lisible (vous pouvez lire la majorité des mots), extrayez tout ce que vous pouvez lire avec confiance. Ne sautez que les **segments (mot, expression, phrase)** ou lignes spécifiques réellement illisibles.

> **LA TRADUCTION FRANÇAISE EST SUR L'IMAGE.** Le champ `"français"` doit être la traduction **imprimée sur la page**, pas celle que vous connaissez. Un même mot breton peut avoir plusieurs sens en français ; seul celui écrit sur l'image compte. Par exemple, `lenn` peut signifier « lac » ou « lecture » — si l'image montre `: le lac`, écrivez `"le lac"`, jamais `"la lecture"`. Ne substituez **jamais** la traduction de l'image par une traduction issue de vos connaissances linguistiques.

### Qualité des scans

Certaines pages peuvent être floues ou mal numérisées, notamment au niveau de la **jointure centrale** (gouttière) entre les deux pages du livre. Le texte situé près de cette zone peut être déformé, tronqué ou illisible. Ignorez les segments spécifiquement tronqués ou illisibles, mais n'utilisez pas la gouttière comme prétexte pour ignorer toute la page.

---

## Disposition des traductions

Les traductions se trouvent selon deux dispositions :

1. **En miroir page gauche / page droite** — la page de gauche est généralement en breton, celle de droite en français (ou vice-versa).
2. **En colonnes gauche / droite sur la même page** — les deux langues sont présentées côte à côte.

Ne conservez **que** les passages où les deux langues sont clairement présentées en regard l'une de l'autre.

---

## Pages à ignorer entièrement

Ignorez sans traitement les pages suivantes :

- Les pages ne comprenant **qu'une seule langue**
- Les pages ne comprenant **pas ou très peu de texte** (couverture, page de garde, pages de chapitre)
- Les pages d'**index**, de **conjugaisons monolingues** ou de **consignes monolingues**, même si elles contiennent quelques mots bretons isolés
- Les pages de **grammaire** où une seule langue est dominante et où l'autre n'est pas une traduction en regard — ne tentez aucun appariement conjectural

---

Certaines sections d'une page bilingue ne constituent pas du contenu parallèle exploitable. Appliquez les exclusions ci-dessous **avec discernement** — l'objectif est d'exclure le contenu qui n'est PAS réellement parallèle, et non de rejeter systématiquement tout ce qui ressemble à un exercice.

> **PRINCIPE CLÉ : Si le contenu d'un exercice contient des équivalents bilingues clairs et alignables (mêmes items, même ordre, même structure), il DOIT être extrait.** Par exemple, si la page gauche liste « ar bluenn-bloum, ar bureo, ar gador » et la page droite liste « le crayon, le bureau, la chaise », ce sont des paires valides même si elles apparaissent dans une section « Exercices d'intuition ».

### Exercices et devoirs à exclure

> 🚨 **ALERTE CRITIQUE : Il est formellement interdit de générer ou deviner la traduction française de ces exercices monolingues.** Si le texte français n'est pas imprimé de manière explicite sur la page, la ligne entière doit être REJETÉE. Démontrez que vous savez lire l'image, pas que vous savez traduire.

Excluez uniquement les exercices qui ne contiennent **pas** de correspondance bilingue exploitable :
- Les sections « **Élocution** », « **Devoir écrit** », « **Deverioù/Devoirs** » quand leur contenu n'a pas d'équivalent dans l'autre langue sur la page en regard
- Les sections « **Thème** » quand une seule langue est lisible ou présente
- Les **exercices à trous** (phrases avec `...` ou mots tronqués) — ils ne constituent pas des traductions complètes
- Les sections avec traductions intercalées entre parenthèses au sein d'une même phrase (ex : « Douaret am eus (j'ai butté) ma betrabez. ») — ce ne sont pas des paires propres
- Les **phrases d'instruction pédagogique** qui introduisent un exercice ou une liste de vocabulaire (ex : `Skrivit ha deskit ar geriou-man : / Ecrivez et apprenez les mots suivants :`, `Skrivit an anoiou-man / Écrivez les noms suivants`) — ce sont des consignes, pas du contenu bilingue exploitable, même si les deux langues sont présentes

### Leçons parallèles non traduites
- Les pages en vis-à-vis qui ne sont **pas des traductions** mais des **leçons parallèles** (même thème traité indépendamment dans chaque langue) — ne tentez aucun alignement hasardeux
- Les sections grammaticales non traduites (conjugaisons, déclinaisons) même si elles apparaissent sur la page en vis-à-vis

### Conjugaisons et listes grammaticales
- Les entrées de **conjugaison** quand une partie de la ligne est tronquée ou illisible dans l'une des deux langues — évitez les paires incomplètes
- Les **tableaux de conjugaison** (1°/2°/3°) : extraction autorisée uniquement quand les deux côtés sont **entièrement lisibles et alignés**

### Contenu illisible
- Les blocs en **corps trop petit** quand l'alignement bilingue devient illisible
- Les sections bilingues dont la **netteté est insuffisante** (contraste/résolution faible) — exclure même si elles semblent en miroir

---

## Règles d'extraction

### Alignement
- Lorsque la ponctuation diverge mais que le contenu est strictement équivalent, autorisez l'alignement « **plusieurs phrases FR ↔ une phrase BR** » (ou l'inverse)
- Pour les listes d'exemples, exigez un **alignement strict item par item** — ne fusionnez pas en une seule paire des listes non strictement parallèles
- Les **titres bilingues** (ex : « Dekvet lennadenn / Dixième lecture ») doivent être inclus s'ils sont clairement en miroir
- Les **légendes** sous les illustrations (ex : « Ar chaseer. — Le Chasseur ») sont des paires bilingues de haute qualité — extrayez-les systématiquement
- Quand le nombre d'items diffère entre les deux langues dans une liste grammaticale, n'extrayez que les lignes manifestement équivalentes

### Découpage
- Découpez systématiquement les paragraphes au niveau des **phrases** (points, points d'interrogation, points d'exclamation)
- Éclatez les paragraphes au niveau des **doubles tirets** `--`
- Vous pouvez éclater au niveau des **points-virgules** `;` si les propositions sont autonomes syntaxiquement et que le découpage fonctionne dans les deux langues
- **Énumérations** : les listes d'éléments séparés par des virgules doivent être éclatées en paires individuelles. Chaque paire doit correspondre à une **unité sémantique et syntaxique** autonome (un mot, une expression, une phrase complète). Par exemple, si la page gauche liste « Tad, mamm, paotr, ki » et la droite « Père, mère, garçon, chien », cela doit produire 4 paires distinctes, **pas** une seule paire contenant toute l'énumération.

### Segments à rejeter
- Ne conservez que les passages **purement bilingues** — ignorez les notes de bas de page, phrases incomplètes, titres seuls, exercices monolingues
- Dès qu'il y a un **déséquilibre sémantique** (ex : phrase bretonne contenant un mot traduit entre parenthèses), sautez la phrase entière
- Les phrases avec traductions intercalées entre parenthèses sur la même ligne doivent être **exclues** même si les deux langues apparaissent
- **Phrases ou mots tronqués en fin de page/colonne** : si une phrase ou une traduction est coupée par la fin de la page de droite, qu'il s'agisse d'une césure, d'un mot incomplet ou d'une définition inachevée, **rejetez entièrement la paire** même si le début est parfaitement lisible. Ne tentez **JAMAIS** de reconstituer la suite ou de deviner/compléter la fin de la traduction.
- **Chaque paire doit faire sens** : les deux côtés (breton et français) doivent être des unités sémantiques complètes et cohérentes. Si une phrase ne fait pas sens (fragment, mot coupé, phrase sans fin), rejetez-la.
- **Noms propres et attributions d'auteur** : excluez les noms propres isolés (noms d'auteurs, de personnes, de lieux sans traduction) ainsi que les lignes de crédit ou signatures en fin de texte (ex : `JAFFRENNOU (Barzaz-Taldir)`, `D'après MATHALIZ`). Ces lignes ne sont pas des paires bilingues exploitables.
- **Mots grammaticaux / non lexicaux** : excluez les paires dont les deux côtés ne sont que des mots-outils sans contenu sémantique autonome — c'est-à-dire les articles, déterminants, prépositions, possessifs, pronoms personnels isolés et particules grammaticales. Ces mots n'expriment que des relations syntaxiques et n'apportent rien au corpus. Exemples de paires à **NE PAS extraire** :
  ```
  {"breton": "va", "français": "mon"}
  {"breton": "d'am", "français": "à mon"}
  {"breton": "da", "français": "ton, ta, tes"}
  {"breton": "e", "français": "son, sa, ses (possesseur masculin)"}
{"breton": "Pe ? -- Peseurt ?", "français": "Quel, quels. .. Quelle, quelles"}
  ```
  En revanche, les **mots lexicaux** (noms, verbes, adjectifs, adverbes) — même courts — restent des paires valides (ex : `{"breton": "ki", "français": "chien"}`).

#### Exemple de paire à NE PAS extraire (phrase tronquée)
```json
{"breton": "Bras e ve abaff ho c'herend pa lakeont e tre daquarn ho bugale pere a gredont desket mad, eur skrit, euz lizer-ferm pe eur c'hountrat all benag pehini o tendues", "français": "Ces jeunes gens sont cependant convaincus qu'ils sont instruits jusqu'à ce que la mise en pratique de leurs pré-"}
```
↑ La phrase française est coupée (« pré- ») → paire invalide, à rejeter.

---

## Normalisation du texte

### Caractères ASCII obligatoires
Les lettres latines de base (`a-z`, `A-Z`) doivent **toujours** être écrites avec des caractères ASCII (U+0041–U+005A, U+0061–U+007A). N'utilisez **jamais** de caractères cyrilliques visuellement similaires (par exemple `е` cyrillique U+0435 au lieu de `e` ASCII U+0065). Les seuls caractères non-ASCII autorisés sont les lettres accentuées françaises et bretonnes (`é`, `è`, `ê`, `ë`, `à`, `â`, `ù`, `û`, `ô`, `ï`, `î`, `ç`, `œ`, `ü`, etc.). Il en va de même pour la ponctuation.

### Ponctuation double
Il est important de **conserver l'espace avant** (et éventuellement après, le cas échéant) les marques de ponctuation doubles (`?`, `!`, `:`, `;`). Ex: `"Pet pousin en deus ar yar-hont ?"` (et non sans espace).

### Espaces syllabiques
Dans ces ouvrages anciens, les syllabes sont fréquemment séparées par des espaces dans l'impression, **aussi bien en breton qu'en français** (ex : `G e o .`, `a no iou tud`, `per son nes`, `ani mal`). **Ne les transcrivez pas tels quels.** Recollez systématiquement ces syllabes pour former des mots complets et normaux.

### Parenthèses et annotations
Supprimez systématiquement :
- Les mentions entre parenthèses (pluriels, alias, indications grammaticales)
- Les marques de genre après les mots (ex : `karo m.` → `karo`, `gad f.` → `gad`)
- Pour `skao (skavenn)`, extraire uniquement `skao`

### Préfixes de dialogue et d'exercice
Supprimez les préfixes de rôle ou de numérotation des dialogues et exercices. Ne conservez que le segment linguistique :
- `G.`, `R.`, `Q.`, `D.`, `M.`, `E.` (marqueurs de rôle dans les dialogues)
- Numérotation (`1.`, `2.`, `a)`, `b)`, etc.)

Exemple : `G. Diskouezit d'in ho fri.` → `Diskouezit d'in ho fri.`

### Orthographe bretonne
Normalisez les variantes d'apostrophes et de diacritiques tout en conservant la fidélité à l'imprimé. En cas de doute sur un caractère, appliquez la règle critique : **ignorez le mot plutôt que deviner**.

### Virgules finales
Supprimez les virgules et point-virgule situées à la toute fin d'un segment extrait. Un segment ne doit **jamais* se terminer par une virgule ou un point-virgule.

### Formes abrégées
Quand une forme féminine bretonne est abrégée ou coupée par la mise en page (ex : suffixe « -ez » séparé), reconstituez le mot complet uniquement si vous en êtes certain.

---

## Format de sortie

### JSONL
Le résultat est un texte brut contenant une ligne par paire au format JSONL valide. **Règle absolue pour l'encodage :** n'utilisez **JAMAIS** de séquences d'échappement Unicode (comme `\u00e9` ou `\u0153`). Vous devez **toujours** fournir les caractères spéciaux (é, œ, à, ñ, etc.) directement formattés en texte brut (UTF-8). :

```json
{"breton": "Ar plac'h vihan a skriv: setu aze pemp ger.", "français": "La petite fille écrit: voilà quatre mots."}
```

### Structure de la réponse

Structurez votre réponse **exactement** comme suit :

```
=== JSONL ===
(uniquement les lignes JSONL, une par paire breton/français, rien d'autre)
=== /JSONL ===

=== RAPPORT ===
Statut: OK | Difficultés | Impossible
Score: <nombre entier entre 0 et 100>
Remarques: <une phrase décrivant les difficultés ou observations>
Observations workflow: Proposez UNIQUEMENT des règles d'extraction qui ne sont PAS déjà couvertes par les instructions ci-dessus. Décrivez le pattern rencontré et la règle manquante. Préfixez chaque suggestion par [GLOBAL] (si la règle s'applique à tous les livres) ou [BOOK] (si elle est spécifique à ce livre). Si toutes les règles sont déjà couvertes, répondez "aucune". Ne répétez PAS des règles déjà documentées.
=== /RAPPORT ===
```

Ne mettez **RIEN** d'autre dans votre réponse.

### Exemples de paires valides

#### Légendes sous illustrations
```json
{"breton": "Ar chaseer", "français": "Le chasseur"}
{"breton": "Ar vamm-goz", "français": "La grand-mère"}
{"breton": "Ar c'honikl", "français": "Le lapin"}
{"breton": "Ar gador", "français": "La chaise"}
```

#### Listes de vocabulaire en miroir (extraire item par item)
Par exemple pour « Tad, mamm, paotr, ki, pesked » / « Père, mère, garçon, chien, poissons » :
```json
{"breton": "Tad", "français": "Père"}
{"breton": "Mamm", "français": "Mère"}
{"breton": "Paotr", "français": "Garçon"}
{"breton": "Ki", "français": "Chien"}
{"breton": "Pesked", "français": "Poissons"}
```

#### Phrases d'exercice en miroir (extraire quand le sens correspond)
```json
{"breton": "Pelec'h eman ar bluenn-bloum?", "français": "Où est le crayon?"}
{"breton": "Ar bluenn-bloum a zo war ar bureo.", "français": "Le crayon est sur le bureau."}
{"breton": "Pelec'h eman ar c'hreiz?", "français": "Où est la craie?"}
{"breton": "Ar c'hreiz a zo aze er voest.", "français": "La craie est là dans la boîte."}
```

#### Mots isolés en miroir
```json
{"breton": "Eun den", "français": "Une personne"}
{"breton": "Eul loen", "français": "Un animal"}
{"breton": "Eun dra", "français": "Une chose"}
```

#### Texte continu en colonnes parallèles (extraire phrase par phrase)
Quand une page présente du texte continu en deux colonnes (ex : préface breton/français), découpez-le en phrases et alignez-les :
```json
{"breton": "Gwelet a rer var armeaz, e ker, kalz krenn-baotred, tud yaouank, o kuitaat skoliou ar c'heriou.", "français": "On voit, dans la Bretagne bretonnante, et notamment dans le Finistère, des élèves de la campagne écrivant passablement l'orthographe."}
```

#### Entrées de type dictionnaire/lexique
Supprimer les marques de genre (f., m., c.), les variantes entre parenthèses, et les abréviations grammaticales :
```json
{"breton": "Kegin", "français": "Cuisine"}
{"breton": "Lestr", "français": "Vase, vaisselle"}
{"breton": "Kontell", "français": "Couteau"}
{"breton": "Loa", "français": "Cuiller"}
{"breton": "Fourchetez", "français": "Fourchette"}
{"breton": "Kambr", "français": "Chambre"}
{"breton": "Gwele", "français": "Lit"}
```

#### Titres bilingues
```json
{"breton": "An annezou", "français": "Les meubles"}
```

---

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
