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

# Instructions spécifiques : Geriadur – Lexique anatomique breton-français (1927)

## Nature de l'ouvrage

Cet ouvrage est un **lexique anatomique et médical** français-breton de 1927. Chaque page contient des **entrées de dictionnaire** dans l'ordre alphabétique, disposées en deux colonnes (pages paires à gauche, impaires à droite). Traitez les deux colonnes séquentiellement.

### Structure d'une entrée

```
mot-vedette français — traduction(s) bretonne(s), marque(s).
```

- Le **mot-vedette français** est en **gras** à gauche
- La **traduction bretonne** se trouve à droite
- Les deux termes sont séparés par un **tiret cadratin** (`—`)
- Des **abréviations grammaticales** suivent les mots : `g.` (genre), `gg.` (pluriel), `av.` (adverbe), `nd.` (nom duel), `l.` (locution/pluriel locatif)

### Sous-entrées

Une entrée peut contenir des **sous-entrées** signalées par un terme abrégé en gras renvoyant au mot-vedette. Par exemple :

```
oblique — beskellek — grand o. : kigenn veskellek bras, gg — petit o. : kigenn veskellek bihan, gg.
```

Ici `grand o.` = `grand oblique` et `petit o.` = `petit oblique`. Chaque sous-entrée est une paire distincte.

---

## Règles d'extraction

### Sens de la traduction

> **ATTENTION** : le mot-vedette (en gras, à gauche) est en **français**, la traduction (à droite, après le tiret cadratin) est en **breton**. Veillez à bien affecter chaque langue au bon champ JSONL.

### Abréviations à omettre

Le début du livre contient une **liste d'abréviations** (par exemple : `ag = ano-gwan`, `as = ano-stroll`, `av = ano-verb`, `g = gourel`, `gg = gwregel`, `l. = lies`, `nd = niver-daou`, `S. = Sellout ouz`). **Ignorez entièrement ces entrées** : elles ne constituent pas des paires bilingues exploitables.

### Développement des abréviations de renvoi

Les sous-entrées abrègent le mot-vedette parent par **sa première lettre suivie d'un point**. La règle est systématique :

> **Quand vous rencontrez `X.` dans une sous-entrée, remplacez-le par le mot-vedette en gras qui ouvre l'entrée courante.**

Ceci s'applique quelle que soit la position dans l'entrée, y compris quand l'entrée s'étend sur plusieurs lignes ou contient de nombreuses sous-entrées.

Exemples courants :

| Entrée parent | Abréviation lue | Développement correct |
|---|---|---|
| **côlon** | `c. ascendant` | `côlon ascendant` |
| **côlon** | `c. transverse` | `côlon transverse` |
| **côlon** | `c. descendant` | `côlon descendant` |
| **côlon** | `S du c.` | `S du côlon` |
| **cuboïde** | `os c.` | `os cuboïde` |
| **cricoïde** | `cartilage c.` | `cartilage cricoïde` |
| **deltoïde** | `muscle d.` | `muscle deltoïde` |
| **déférent** | `canal d.` | `canal déférent` |
| **dentaire** | `alvéole d.` | `alvéole dentaire` |
| **oblique** | `grand o.` | `grand oblique` |
| **oblique** | `petit o.` | `petit oblique` |
| **obturateur** | `trou o.` | `trou obturateur` |
| **occipital** | `os o.` | `os occipital` |
| **olfactif** | `nerf o.` | `nerf olfactif` |
| **optique** | `nerf o.` | `nerf optique` |
| **orteil** | `gros o.` | `gros orteil` |
| **papille** | `p. du goût` | `papille du goût` |
| **pathétique** | `nerf p.` | `nerf pathétique` |
| **coxo-fémoral** | `articulation c.` | `articulation coxo-fémorale` |
| **visuel** | `acuité v.` | `acuité visuelle` |
| **visuel** | `angle v.` | `angle visuel` |
| **vocal** | `corde v.` | `corde vocale` |
| **voile** | `v. du palais` | `voile du palais` |
| **pituitaire** | `membrane p.` | `membrane pituitaire` |
| **pituitaire** | `glande p.` | `glande pituitaire` |

### Synonymes bretons multiples

Quand une entrée a plusieurs traductions bretonnes séparées par des virgules, **éclatez chaque synonyme en une paire distincte** associée au même mot français. Chaque traduction bretonne doit produire sa propre ligne JSONL.

### Traductions directes vs. gloses descriptives

Certaines entrées contiennent un mot breton direct suivi d'une longue phrase descriptive en breton (description anatomique). Ne gardez que le mot direct — la phrase descriptive n'est pas un synonyme exploitable.

Exemple : `côlon — kolon, g, eil kevrenn ar vou-zellenn deo, gg` → garder uniquement `kolon` (le reste est une glose « deuxième section de l'intestin »).

### Segments bretons de plus de 3 mots

**Ignorez tout segment breton comptant plus de 3 mots** (en comptant les mots séparés par des espaces). Ces segments longs sont des définitions ou explications anatomiques, pas des traductions exploitables.

Exemples à ignorer :
- `kevrenn genta ar vouzellenn deo` (glose pour « caecum »)
- `kenta kevrenn ar vouzellenn voan` (glose pour « duodénum »)
- `eil kevrenn ar vouzellenn deo` (glose pour « côlon »)

### Renvois « S. » (synonyme)

Certaines entrées renvoient à un autre mot via `S.` (synonyme). **Ignorez ces entrées** — elles ne contiennent pas de traduction bretonne propre.

Exemple à ignorer : `ombilie — S. nombril.`

### Abréviations grammaticales à supprimer

Supprimez de la sortie : `g.`, `gg.`, `av.`, `nd.`, `l.`, et toute abréviation grammaticale après le mot breton.

### Parenthèses de précision en français

Conservez les précisions entre parenthèses dans le champ français quand elles désambiguïsent le terme :
- `couche (graisseuse, etc.)` ✅
- `creux (de la main)` ✅
- `détroit (du bassin)` ✅
- `oreillette (du cœur)` ✅
- `ventricule (du cœur)` ✅
- `pavillon (de l'oreille)` ✅
- `poil (du corps)` ✅
- `plante (du pied)` ✅
- `plancher (de la bouche)` ✅

### Formes dérivées avec tiret-préfixe

Quand une variante bretonne est indiquée par un tiret-préfixe seul (ex : `-kilpenn` sous `kilpennel`), cela indique une racine ou un suffixe — **ignorez ces fragments**. Gardez uniquement les formes complètes et autonomes.

### Entrées composées avec plusieurs sous-entrées en ligne

Certaines entrées contiennent l'adjectif principal suivi de plusieurs sous-entrées sur les lignes suivantes, chacune avec un qualificatif en gras. Par exemple :

```
visuel — ar gweled — acuité v. : lemm-der-gweled — angle v. : kornad-gweled
```

Extrayez :
1. L'entrée principale : `{"breton": "ar gweled", "français": "visuel"}`
2. Chaque sous-entrée avec le terme développé

### Tiret composé (trait d'union long)

Certains mots bretons composés utilisent un tiret long (`-ha-`, `-ar-`). Conservez-les tels quels :
- `skevent-ha-kreuz` → garder intégralement
- `skevent-ha-sac'h-boued` → garder intégralement

---

## Exemples complets

Voici comment extraire des entrées typiques de ce lexique :

### Entrée simple
Image : `cou — gouzoug, g.`
```json
{"breton": "gouzoug", "français": "cou"}
```

### Entrée avec précision contextuelle et synonymes
Image : `couche — (graisseuse, etc.) gwiskad, g, gwelead, g.`
```json
{"breton": "gwiskad", "français": "couche (graisseuse)"}
{"breton": "gwelead", "français": "couche (graisseuse)"}
```

### Entrée avec sous-entrées abrégées
Image : `oblique — beskellek — grand o. : kigenn veskellek bras, gg — petit o. : kigenn veskellek bihan, gg.`
```json
{"breton": "beskellek", "français": "oblique"}
{"breton": "kigenn veskellek bras", "français": "grand oblique"}
{"breton": "kigenn veskellek bihan", "français": "petit oblique"}
```

### Entrée avec une seule sous-entrée
Image : `déférent — diskarg — canal d. : kansper, g.`
```json
{"breton": "diskarg", "français": "déférent"}
{"breton": "kansper", "français": "canal déférent"}
```

### Entrée longue avec nombreuses sous-entrées (côlon)
Image : `côlon — kolon, g, eil kevrenn ar vou-zellenn deo, gg — c. ascendant : bann-sevel ar c'holon, g. — c. transverse : treuzell ar c'holon, gg — c. descendant : bann-diskenn ar c'holon, g. — S du c. : S ar c'holon, g.`

> Le mot-vedette est `côlon`. Toute occurrence de `c.` dans les sous-entrées doit être développée en `côlon` :
```json
{"breton": "kolon", "français": "côlon"}
{"breton": "bann-sevel ar c'holon", "français": "côlon ascendant"}
{"breton": "treuzell ar c'holon", "français": "côlon transverse"}
{"breton": "bann-diskenn ar c'holon", "français": "côlon descendant"}
{"breton": "S ar c'holon", "français": "S du côlon"}
```

### Entrée avec nom duel
Image : `œil — lagad, g, nd. daoulagad.`
```json
{"breton": "lagad", "français": "œil"}
```

### Entrée avec locution pluriel
Image : `organe — benveg, g, l. binviou, benvegenn, gg.`
```json
{"breton": "benveg", "français": "organe"}
{"breton": "binviou", "français": "organe"}
{"breton": "benvegenn", "français": "organe"}
```

### Entrée renvoi (à ignorer)
Image : `ombilie — S. nombril.`
→ **Ne pas extraire** (renvoi synonymique, pas de traduction)

### Entrée avec qualificatif de sous-type

Image : `pectoral — -brennid — grand p. : kigenn-vrennid vras, gg — petit p. : kigenn-vrennid vihan, gg.`

> Le mot-vedette `pectoral` n'a qu'un fragment breton (`-brennid`) — **ignorez l'entrée principale** (fragment inutilisable). Extrayez uniquement les sous-entrées complètes :
```json
{"breton": "kigenn-vrennid vras", "français": "grand pectoral"}
{"breton": "kigenn-vrennid vihan", "français": "petit pectoral"}
```

### Entrée avec locution composée

Image : `vocal — mouezel, -mouez — corde v. : korden-vouez, l. kerdin-mouez.`

> Gardez le mot complet (`mouezel`), **supprimez le fragment** (`-mouez`) :
```json
{"breton": "mouezel", "français": "vocal"}
{"breton": "korden-vouez", "français": "corde vocale"}
{"breton": "kerdin-mouez", "français": "corde vocale"}
```

### Fin du dictionnaire

La dernière page se termine par un trait décoratif (`——w——`). **Ignorez** ces marques de fin de section.

### Qualité du scan

Ce lexique de 1927 est globalement bien imprimé. Les caractères sont nets dans la grande majorité des cas. La jointure centrale peut affecter quelques mots — ignorez uniquement ceux qui sont réellement illisibles.
