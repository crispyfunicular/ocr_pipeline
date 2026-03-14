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
{"breton": "Setu a hont an daolenn", "français": "Voilà là-bas le tableau"}
{"breton": "an nor", "français": "la porte"}
{"breton": "ar prenestr", "français": "la fenêtre"}
```

### Lennadennou / Lectures
Les pages de lecture présentent des textes en vers ou en prose numérotés (1., 2., 3., …), avec le breton à gauche et le français à droite. Extrayez **strophe par strophe** — chaque strophe numérotée constitue un segment. Ne découpez pas ligne par ligne à l'intérieur d'une strophe :

> **EXCEPTION UNIQUE** : c'est le seul et unique cas où la règle globale de découpage au niveau des phrases (points, `?`, `!`) peut être contournée. Les strophes numérotées de ce livre constituent des segments indivisibles.

```json
{"breton": "Eun amzer a zo bet, ha ne veze klevet 'N hon touez nemet yez Breiz ; war ar maez, 'vel en kêr, Holl 'komzemp ar yez koz gant hon tadou komzet, En Gwened, en Kerne, Leon ha Landreger.", "français": "Il fut un temps, où l'on n'entendait, parmi nous, que la langue de Breiz : à la campagne comme en ville, nous parlions tous la vieille langue que parlaient nos pères, en Vannes, en Cornouaille, en Léon, en Trégor."}
```

### Sections à exclure

- **Devoir / Devoir écrit** : exercices à compléter, souvent monolingues → **exclure**
- **Notes grammaticales** en bas de page (numérotées `(1)`, `(2)`) : explications de règles → **exclure**
- **Exercices « Skrivet hag echuit ar gerion-man »** (Écrire et compléter les mots suivants) → **exclure** (monolingue, phrases à trous)
- **Sections « Grammaire »** en bas de page droite → **exclure** (consignes monolingues)
- **Sections « Verbou / Verbes »** — **conjugaisons avec paradigmes** (1°, 2°, 3°) → **exclure**. En revanche, quand une section Verbou est une simple **liste de vocabulaire** (infinitif breton + traduction française, sans paradigmes), **extraire** comme n'importe quelle liste de vocabulaire. Même règle pour « Anoïou gwan / Adjectifs » : extraire les listes breton/français.
- **Tableaux de pronoms, déterminants et mots grammaticaux** (ex : *Raganoiou staga* / Pronoms relatifs, *Raganoiou damziskoueza* / Pronoms indéfinis) → **exclure entièrement** (conformément à la règle globale sur les mots-outils). Exemples de paires à **NE PAS extraire** :
  ```
  {"breton": "hini ebet, den ebet, nikun", "français": "aucun, nul, personne"}
  {"breton": "pep hini, peb unan", "français": "chacun, chacune"}
  {"breton": "an hevelep", "français": "le même, la même"}
  {"breton": "me end-eeun", "français": "moi-même"}
  ```
- **Sections « Thème » / « Da lakat e galleg »** : exercices de traduction dirigés → **exclure** (monolingues ou semi-monolingues)
- **Phrases d'instruction pédagogique** : les consignes qui introduisent un exercice ou une liste (ex : `Skrivit ha deskit ar geriou-man : / Ecrivez et apprenez les mots suivants :`) → **exclure**. Ce ne sont pas des paires bilingues exploitables pour le corpus, même si les deux langues sont présentes.
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
