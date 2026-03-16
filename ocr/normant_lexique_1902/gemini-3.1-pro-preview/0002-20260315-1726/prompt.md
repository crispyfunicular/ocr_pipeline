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
