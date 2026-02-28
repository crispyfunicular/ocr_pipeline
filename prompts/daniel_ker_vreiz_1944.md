# Instructions spécifiques : Daniel – Ker Vreiz, Cours de breton (1944)

## Nature de l'ouvrage

Cet ouvrage est un **cours de breton** de 1944 organisé en leçons numérotées (KENTEL I, KENTEL II, etc.). Chaque leçon contient :

1. **VOCABULAIRE** : liste de mots breton ↔ français avec prononciation entre parenthèses
2. **GRAMMAIRE** : règles grammaticales avec exemples bilingues intégrés
3. **Tableaux de conjugaison** : verbes conjugués en breton et français en colonnes alignées
4. **Remarques** et règles encadrées

### Disposition

Chaque page-scan contient deux pages imprimées côte à côte. Les deux pages appartiennent souvent à la même leçon et ne sont pas nécessairement en opposition bilingue (gauche ≠ breton, droite ≠ français). Le contenu bilingue se trouve **au sein de chaque page**, dans les vocabulaires et exemples.

---

## Règles d'extraction

### Vocabulaire

Les blocs « VOCABULAIRE » listent des mots avec le format :
```
Mot breton : traduction française
```

Extrayez chaque paire :
```json
{"breton": "Loeiz", "français": "Louis"}
{"breton": "an tan", "français": "le feu"}
{"breton": "ar stered", "français": "les étoiles"}
{"breton": "ar heol", "français": "le soleil"}
{"breton": "al loar", "français": "la lune"}
```

### Nettoyage du vocabulaire

- **Prononciation entre parenthèses** : `(-ou)`, `(-iou)`, `(-eu)` → **supprimer**
  - `ar c'h/koumoul (e)` → `ar c'houmoul`
  - `an endervez (m) (-iou)` → `an endervez`
- **Marques de genre** : `(m)`, `(f)`, `(e)` → **supprimer**
- **Formes verbales** après un verbe : par exemple `diskar (diskaret)` → extraire `diskar`

### Mutations consonantiques initiales

Le breton possède un système de **mutations des consonnes initiales**. Dans cet ouvrage, les mots mutés sont notés avec une barre oblique : `consonne_mutée/consonne_radicale + reste_du_mot`.

#### Règle mécanique de résolution

Quand vous voyez une notation `X/Yzzz` au début d'un mot (où `X` est la consonne mutée, `Y` la consonne radicale, et `zzz` le reste du mot) :

1. **Supprimer** la barre oblique `/` et la consonne radicale `Y`
2. **Garder** uniquement la consonne mutée `X` collée au reste du mot `zzz`
3. Résultat : `Xzzz`

Procédure pas à pas :
```
g/kanaouenn  →  supprimer « /k »  →  ganaouenn
g/kontadenn  →  supprimer « /k »  →  gontadenn
w/gwirionez  →  supprimer « /gw » →  wirionez
w/gwech      →  supprimer « /gw » →  wech
c'h/koumoul  →  supprimer « /k »  →  c'houmoul
c'h/kar      →  supprimer « /k »  →  c'har
b/plijadur   →  supprimer « /p »  →  blijadur
v/bro        →  supprimer « /b »  →  vro
v/mamm       →  supprimer « /m »  →  vamm
z/dor        →  supprimer « /d »  →  zor
d/tad        →  supprimer « /t »  →  dad
f/penn       →  supprimer « /p »  →  fenn
```

#### Exemples complets avec contexte (entrée image → sortie JSONL)

```
ar g/kanaouenn (-ou) : la chanson   →  {"breton": "ar ganaouenn", "français": "la chanson"}
ar g/kontadenn (-ou) : le conte     →  {"breton": "ar gontadenn", "français": "le conte"}
ar w/gwirionez (-iou) : la vérité   →  {"breton": "ar wirionez", "français": "la vérité"}
ar w/gwech (-ou) : la fois          →  {"breton": "ar wech", "français": "la fois"}
ar c'h/koumoul (e) : les nuages    →  {"breton": "ar c'houmoul", "français": "les nuages"}
ar c'h/kar : le parent              →  {"breton": "ar c'har", "français": "le parent"}
ar g/ker : la ville                 →  {"breton": "ar ger", "français": "la ville"}
ar b/plijadur : le plaisir          →  {"breton": "ar blijadur", "français": "le plaisir"}
ar v/bro : le pays                  →  {"breton": "ar vro", "français": "le pays"}
ar v/mamm : la mère                 →  {"breton": "ar vamm", "français": "la mère"}
ar z/dor : la porte                 →  {"breton": "ar zor", "français": "la porte"}
ar d/tad : le père                  →  {"breton": "ar dad", "français": "le père"}
```

⚠️ **Ne JAMAIS reproduire la barre oblique `/` ni la consonne radicale dans le JSONL de sortie.** Si le résultat contient un `/`, c'est une erreur.

### Exemples grammaticaux

La section GRAMMAIRE contient des règles en français avec des exemples bilingues. Extrayez **uniquement** les exemples clairement bilingues marqués par `Ex.` :
```json
{"breton": "ar c'houmoul", "français": "les nuages"}
{"breton": "ar ger", "français": "la ville"}
{"breton": "ar blijadur", "français": "le plaisir"}
{"breton": "eur goumoulenn", "français": "un nuage"}
{"breton": "eur steredenn", "français": "une étoile"}
```

### Tableaux de conjugaison

Les tableaux montrent les formes conjuguées en deux langues. Extrayez chaque ligne comme une paire **uniquement quand les deux colonnes sont complètes et lisibles** :
```json
{"breton": "Me a zo bras", "français": "Je suis grand"}
{"breton": "Te a zo bihan", "français": "Tu es petit"}
{"breton": "Eñ a zo kozh", "français": "Il est vieux"}
```

Les encadrés contiennent des règles grammaticales en français (ex : « *Les pronoms relatifs « a » et « na » provoquent les mutations ordinaires.* »). Ils ne constituent pas des paires bilingues → **exclure**.

### Sections à exclure

- **Remarques** = explications grammaticales monolingues → **exclure**
- **Règles numérotées** (1re Règle, 2e Règle, etc.) avec exemples purement grammaticaux sans traduction → **exclure**
- **Textes de lecture** « LENNADENN » = texte continu monolingue breton → **exclure** entièrement. Même si le texte contient des mots français en italique entre parenthèses (ex. « *pour le soigner* », « *littéralement* »), ces éléments sont des gloses contextuelles, pas des traductions systématiques
- **POELLADENNOU** (exercices) → **exclure** entièrement — les sections « Traduisez » et « Répondez en breton » sans réponse fournie ne sont pas exploitables
- **Conjugaison sans colonne française** : les formes de verbe `a so` avec situation (emaout, emaomp...) sans traduction en regard → **exclure**

### Qualité du scan et règle de lecture stricte

Certaines pages ou zones de ce livre sont floues ou en petit corps. Appliquez les règles suivantes **sans exception** :

1. **LIRE, ne jamais deviner.** Chaque mot breton et français extrait doit être **lu directement sur l'image**, caractère par caractère. Ne complétez jamais un mot à partir de vos connaissances linguistiques du breton ou du français.
2. **Certitude à 100 %.** Si un mot, une lettre ou un accent n'est pas lisible avec une certitude absolue, **omettez la paire entière**. Il vaut mieux perdre une paire que d'en inventer une fausse.
3. **Pas de substitution.** Ne remplacez jamais un mot illisible par un synonyme ou un mot proche qui « aurait du sens ». Par exemple, si vous lisez `ar souez` sur l'image, n'écrivez pas `ar geiz` même si les deux pourraient signifier quelque chose de similaire.
4. **Pas d'invention.** N'ajoutez jamais de paires qui n'apparaissent pas explicitement sur la page. Chaque ligne du JSONL doit correspondre à une entrée visible sur l'image.
5. **Orthographe exacte.** Recopiez l'orthographe exacte telle qu'elle apparaît sur l'image, y compris les lettres finales (ex : `beure` et non `beur`, `lenn` et non `len`).
6. **La traduction française est sur l'image.** Le champ `"français"` doit être la traduction **imprimée sur la page**, pas celle que vous connaissez. Un même mot breton peut avoir plusieurs sens ; seul celui écrit sur l'image compte. Exemple : `lenn` peut signifier « lac » ou « lecture » — si l'image montre `: le lac`, écrivez `"le lac"`, jamais `"la lecture"`.
