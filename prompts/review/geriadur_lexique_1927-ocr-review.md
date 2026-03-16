# Critères de révision spécifiques : Geriadur Lexique 1927

## Nature de l'ouvrage

Lexique d'anatomie bilingue français-breton, 18 pages, format alphabétique en 2 colonnes. Spécialité médicale.

## Vérifications spécifiques

### Redirections `S.` (capital)

Le dictionnaire utilise `S.` (= *Sellout ouz*, « voir ») pour les renvois synonymiques. Ces entrées ne contiennent **aucune traduction bretonne propre** et doivent être **exclues** du JSONL.

**Vérifier** :
- [ ] Aucune entrée avec `S.` dans le champ français n'apparaît dans le JSONL
- [ ] Les mots cibles des renvois sont bien extraits sous leur propre vedette

**Attention** : Ne pas confondre avec `s.` (minuscule) qui est une abréviation de première lettre du mot vedette et **doit** être expansée (ex : sous `salivaire`, `glandes s.` → `glandes salivaires`).

### Expansion des sous-entrées

Les sous-entrées utilisent la première lettre du mot vedette suivie d'un point comme abréviation. Le réviseur doit vérifier que ces abréviations sont correctement résolues.

Exemples :
- Sous `saphène` : `veine s.` → `veine saphène` ✅
- Sous `scalène` : `muscle s.` → `muscle scalène` ✅
- Sous `sous-clavière` : `artère s.` → `artère sous-clavière` ✅

### Filtre des glosses bretonnes longues

Le prompt livre impose d'exclure les paires dont le champ breton dépasse **3 mots**. Vérifier que cette règle est appliquée :
- `nerf pathétique` → Breton `pevare koublad an nervennou-klopen` (4+ mots) → **exclu** ✅
- `nerf optique` → Breton `nervenn al lagad` (3 mots) → **inclus** ✅

### Fragments avec tiret

Les formes en `-prefix` (ex : `-kalon`, `-penn`, `-empenn`) sont des fragments morphologiques, pas des mots autonomes. Vérifier qu'elles sont exclues.

### Colonnes inversées

Sur les pages d'introduction et de préface (si présentes), les colonnes breton/français peuvent être inversées par rapport au corps du dictionnaire. Vérifier que les champs ne sont pas intervertis.

### Marques de genre

Les marques `m.`, `f.`, `c.` doivent être supprimées des deux champs. Vérifier l'absence de résidus.
