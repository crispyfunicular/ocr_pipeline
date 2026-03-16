# Critères de révision spécifiques : Daniel — Ker Vreiz (1944)

## Nature de l'ouvrage

Cours de breton organisé en leçons numérotées (KENTEL). Contient du vocabulaire, de la grammaire, des exercices et des tableaux de conjugaison. Le contenu bilingue se trouve **au sein de chaque page** (pas en vis-à-vis gauche/droite).

## Vérifications spécifiques

### Résolution des mutations consonantiques (`/`)

Le livre utilise la notation `X/Yzzz` pour les mutations initiales. Le réviseur **doit** vérifier qu'aucune barre oblique (`/`) ne subsiste dans le champ breton.

**Vérifier** :
- [ ] Aucun champ `breton` ne contient le caractère `/`
- [ ] Les mutations sont correctement résolues (ex : `g/kanaouenn` → `ganaouenn`, `c'h/koumoul` → `c'houmoul`)
- [ ] Le digraphe `gw → w` est géré (ex : `w/gwern` → `wern`)
- [ ] Le cas `g → Ø` est géré (ex : `o/gouel` → `ouel`, **pas** `oouel`)

### Marqueurs de prononciation

Les indicateurs `(-ou)`, `(-iou)`, `(-eu)`, `(m)`, `(f)`, `(e)` doivent être supprimés.

**Vérifier** :
- [ ] Aucun marqueur de prononciation résiduel entre parenthèses
- [ ] Aucune marque de genre résiduelle

### Synonymes français

Quand un mot breton a plusieurs traductions françaises séparées par une virgule (ex : `brao : beau, joli`), elles doivent rester **ensemble** dans un seul champ : `"beau, joli"`. Le réviseur doit s'assurer qu'elles n'ont **pas** été éclatées en paires séparées.

### Exclusions

**Vérifier** que les sections suivantes sont correctement exclues :
- [ ] **LENNADENN** (lectures monolingues bretonnes) — même avec des gloses entre parenthèses
- [ ] **POELLADENNOU** (exercices) — pas de paires inventées
- [ ] **Remarques** / Règles grammaticales monolingues
- [ ] **Marqueurs `etc.`** — aucune paire ne se termine par `etc.`

### Tableaux singulier/pluriel

Quand le vocabulaire montre la forme radicale + forme mutée + pluriel, vérifier que **seules les formes avec article** sont extraites :
- `kaier — ar c'haier : le cahier` → `ar c'haier → le cahier` ✅
- Forme nue `kaier` seule → **exclue** ✅

### Tableaux de conjugaison

Vérifier que les conjugaisons sont extraites **uniquement** quand les deux colonnes (breton + français) sont complètes et lisibles.
