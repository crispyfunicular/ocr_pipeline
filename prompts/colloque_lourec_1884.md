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
