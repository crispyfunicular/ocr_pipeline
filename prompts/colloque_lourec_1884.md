# Instructions spécifiques : Colloque français et breton – Le Lourec (1884)

## Nature de l'ouvrage

Cet ouvrage est un **colloque bilingue** (phrasebook) de 1884, très similaire au Colloque de 1890. Il contient :

- Des **listes de vocabulaire par métier/profession** en 4 colonnes (BR1 | FR1 | BR2 | FR2)
- Des **dialogues conversationnels** avec phrases parallèles français ↔ breton
- Des **listes de verbes** en colonnes parallèles

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

### Synonymes avec « ou »

Conservez les variantes avec « ou » dans le même champ :
```json
{"breton": "Farsal ou caquetal", "français": "Badiner"}
{"breton": "Argumenti ou Argusi", "français": "Argumenter"}
{"breton": "Senni ou Sonn", "français": "Sonner (les cloches)"}
```

### Indications entre parenthèses en français

Les précisions entre parenthèses en français qui désambiguïsent le sens doivent être conservées :
```json
{"breton": "Moula ou Imprima", "français": "Imprimer"}
{"breton": "Composi", "français": "Composer (terme d'imprimerie)"}
{"breton": "Dilivra", "français": "Délivrer (donner)"}
{"breton": "Dilivria", "français": "Délivrer (de captivité)"}
```

### Dialogues conversationnels

Mêmes règles que le Colloque de 1890 : extrayez chaque paire de phrases parallèles indépendamment.

### Sections à exclure

- Les en-têtes « COLLOQUE » / « FRANÇAIS ET BRETON » → **exclure**
- Les parenthèses contenant « prendre balais » ou autres précisions d'action → conserver si elles désambiguïsent

### Qualité du scan

Similaire au Colloque de 1890. Le texte est petit mais net. Les séparateurs de colonnes sont visibles.
