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

# Instructions spécifiques : Colloque français et breton – Le Lourec (1884)

## Nature de l'ouvrage

Cet ouvrage est un **colloque bilingue** (phrasebook) de 1884, très similaire au Colloque de 1890. Il contient :

- Des **listes de vocabulaire par métier/profession** en 4 colonnes (BR1 | FR1 | BR2 | FR2)
- Des **dialogues conversationnels** avec phrases parallèles français ↔ breton
- Des **listes de verbes** en colonnes parallèles
- Un **lexique breton-français** en deux colonnes : français à gauche, traduction bretonne à droite

Les pages sont organisées par profession : « Du Maçon », « Du Charpentier », « Du Couvreur », etc.

---

## Règles d'extraction

### Listes de vocabulaire en 4 colonnes

Identiques au Colloque de 1890 : traitez chaque paire (colonnes 1/2) et (colonnes 3/4) indépendamment.

```json
{"breton": "Parlant", "français": "Parler"}
{"breton": "Caret", "français": "Aimer"}
{"breton": "Dibri", "français": "Manger"}
{"breton": "Ehana", "français": "S'arrêter"}
{"breton": "Coumandi", "français": "Commander"}
```

### Titres de profession

Les en-têtes de section par métier sont parfois bilingues. Extrayez uniquement les titres qui constituent une **vraie paire lexicale** (ex : nom de métier) :
```json
{"breton": "Ar Masson", "français": "Le Maçon"}
{"breton": "Ar C'harpanter", "français": "Le Charpentier"}
```

> **Ignorez** les titres organisationnels longs (ex : « Des Verbes les plus nécessaires du 1er ordre ») — ce sont des métadonnées, pas des unités sémantiques.
- **Mots grammaticaux / non lexicaux** : excluez les paires dont les deux côtés ne sont que des mots-outils sans contenu sémantique autonome — c'est-à-dire les articles, déterminants, prépositions, possessifs, pronoms personnels isolés et particules grammaticales. Ces mots n'expriment que des relations syntaxiques et n'apportent rien au corpus. Exemples de paires à **NE PAS extraire** :
  ```
  {"breton": "va", "français": "mon"}
  {"breton": "d'am", "français": "à mon"}
  {"breton": "da", "français": "ton, ta, tes"}
  {"breton": "e", "français": "son, sa, ses (possesseur masculin)"}
{"breton": "Pe ? -- Peseurt ?", "français": "Quel, quels. .. Quelle, quelles"}
  ```
  En revanche, les **mots lexicaux** (noms, verbes, adjectifs, adverbes) — même courts — restent des paires valides (ex : `{"breton": "ki", "français": "chien"}`).
- **Énumérations d'exemples non traduits** : excluez les passages (comme dans les introductions grammaticales) où le français se contente de répéter une énumération de mots bretons sans fournir de traduction.
  - *À REJETER :* `{"breton": "Quentel : Bep, pep, dad, tad... etc.", "français": "Exemples : Bep, pep, dad, tad... etc."}`

### Synonymes avec « ou »

Quand un mot breton ou français présente des variantes avec « ou » ou « , » (virgule), créez une entrée distincte pour chaque variante :

```json
{"breton": "Farsal", "français": "Badiner"}
{"breton": "Caquetal", "français": "Badiner"}
{"breton": "Argumenti", "français": "Argumenter"}
{"breton": "Argusi", "français": "Argumenter"}
```

### Indications entre parenthèses en français

Les précisions entre parenthèses en français qui désambiguïsent le sens ne doivent pas être conservées.  
NE PAS ECRIRE :
```json
{"breton": "Composi", "français": "Composer (terme d'imprimerie)"}
```

### Lexique breton-français (pages en deux colonnes)

Certaines pages sont organisées en **lexique bilingue** avec deux colonnes :
- **Colonne de gauche** : le mot ou l'expression en **français**
- **Colonne de droite** : la traduction en **breton**, en regard

Extrayez chaque paire comme une entrée indépendante, toujours avec le **breton en premier** :
```json
{"breton": "Tra", "français": "Chose"}
{"breton": "Merc'h", "français": "Fille"}
{"breton": "Tad", "français": "Père"}
```

**Règles spécifiques au lexique :**

1. **Ignorer les points après un mot isolé.** Si un mot est suivi d'un point (ex : `Chose.` → `Chose`), supprimez le point. Ne conservez la ponctuation finale que s'il s'agit réellement d'une **phrase complète** (sujet + verbe).
2. **Exclure tout ce qui n'a pas de traduction directe** dans l'autre langue. Si une entrée de la colonne gauche n'a pas de correspondant visible dans la colonne droite (ou inversement), ignorez-la.
3. **Exclure les en-têtes de catégorie** qui ne constituent pas une paire lexicale (ex : titres de section thématiques sans traduction en regard).
4. **Tirets cadratins (—).** Quand une entrée commence par un tiret cadratin (`—` ou `–`), celui-ci remplace le mot-clé de la catégorie en cours. Remplacez le tiret par ce mot-clé pour reconstituer l'expression complète. Par exemple, sous la catégorie « De la Terre » / « Eur an Douar » :
   - `— grasse` / `— druz` → extraire `{"breton": "Douar druz", "français": "Terre grasse"}`
   - `— stérile` / `— difrouer` → extraire `{"breton": "Douar difrouer", "français": "Terre stérile"}`
   - `— glissante` / `— risclus` → extraire `{"breton": "Douar risclus", "français": "Terre glissante"}`

### Dialogues et phrases courtes en regard

Mêmes règles que le Colloque de 1890 : extrayez chaque paire de phrases parallèles indépendamment. 
À partir de la page 26, ce sont de petites phrases qui sont mises en regard. Il faut conserver la même logique que pour les listes de vocabulaire : chaque ligne (physique) correspond à une paire (de phrases) breton-français. Extraire ces phrases par paires.

### Textes longs en regard (pages 2 à 3)

Dans les toutes premières pages, on trouve de longs textes introductifs mis côte à côte :
- **Attention :** le français se trouve dans la colonne de gauche, et le breton dans la colonne de droite.
- Il faut associer la première phrase en français (à gauche) à la première phrase en breton (à droite), et ainsi de suite.
- En cas de doute sur la correspondance, **ignorez la phrase en question**.
- Si une phrase se trouve à cheval sur deux pages et apparaît comme tronquée en haut à gauche ou en bas à droite, il faut **l'IGNORER entièrement**. Ne cherchez jamais à deviner le début ou la fin d'une phrase qui serait tronquée.

### Textes longs en regard (à partir de la page 60)

À partir de la page 60, ce sont des textes plus longs qui sont mis en regard. 
- Il faut tâcher de faire se correspondre la première phrase (en breton) à gauche avec la première phrase (en français) à droite, et ainsi de suite.
- En cas de doute, ignorez la phrase en question.
- Si une phrase se trouve à cheval sur deux pages et se trouve tronquée en bas à droite ou en haut à gauche, ignorez-la également. Ne cherchez jamais à deviner par vous-même la suite d'une phrase.
- **Points de suspension (...) :** À partir de la page 63, les segments contiennent parfois des points de suspension `...` au milieu des phrases (par exemple : `{"breton": "D'an Autrou, An autrou....., marc'hadour e,.....", "français": "A Monsieur, Monsieur....., marchand à....."}`). **Ne conservez PAS ces segments.** Les points de suspension ne sont acceptés que s'ils se situent uniquement à la toute fin de la phrase.

### Sections à exclure

- Les en-têtes « COLLOQUE » / « FRANÇAIS ET BRETON » → **exclure**
- Les parenthèses contenant « prendre balais » ou autres précisions d'action → conserver si elles désambiguïsent

### Table des matières (pages 69 à 72)

Pour les pages constituant la table des matières (pages 69 à 72) :
- **Ne conservez AUCUNE numérotation.** 
- Supprimez les chiffres romains situés au début de la ligne (ex: `XXII.`, `XXIII.`, `I.`, `V.`).
- Supprimez les chiffres arabes situés à la fin de la ligne (les numéros de page, ex: `94`, `95`).
- Supprimez les points de suite (`......`).
- **Ignorez les lignes contenant uniquement une abréviation de répétition** (par exemple `Id.`).
- N'extrayez que le texte du titre de la section.
  - *Exemple source FR:* `XXII. Dialogue entre un frère et une sœur ............ 94`
  - *Exemple source BR:* `XXII. Dialog etre eur breur hag eur c'hoar ............ 94`
  - *Extrait attendu:* `{"breton": "Dialog etre eur breur hag eur c'hoar", "français": "Dialogue entre un frère et une sœur"}`

### Qualité du scan

Similaire au Colloque de 1890. Le texte est petit mais net. Les séparateurs de colonnes sont visibles.
