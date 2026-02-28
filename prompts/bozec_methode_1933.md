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
> Supprimez les annotations grammaticales entre parenthèses dans les titres (ex : `(ien, ed, ou)`, `(s, x, aux)`).

### Sections Élocution
Ces sections contiennent du texte continu. Le breton est sur la page de gauche, le français sur la page de droite. **Alignez phrase par phrase** en découpant aux points et aux doubles tirets `--`. Les phrases doivent se correspondre dans les deux langues.

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
- **Sections « Thème » / « Da lakat e galleg »** : exercices de traduction dirigés → **exclure** (monolingues ou semi-monolingues)

### Nettoyage

- **Indications de prononciation** entre parenthèses : `(-ou)`, `(-iou)`, `(-eu)` → supprimer
- **Marques de genre** : `(m)`, `(f)`, `(e)` → supprimer
- Les mots de vocabulaire incluent parfois la mutation après un article : `an oabl (m) (-ou)` → extraire simplement `an oabl`
- **Numérotation de leçon** (ex. `Kentel 3`, `Leçon 3`) → supprimer du contenu extrait, mais extraire le titre de la leçon s'il est bilingue
- **Marques typographiques** : les marques `▶`, `♦`, `•` ou équivalents d'imprimerie ancienne utilisés comme séparateurs → ignorer

### Qualité du scan

Les pages sont généralement bien imprimées avec des illustrations claires. La jointure centrale peut légèrement affecter le texte — ignorez uniquement les mots réellement illisibles.
