# Instructions spécifiques : Roparz – Cours élémentaire de breton (1930)

## Nature de l'ouvrage

Cet ouvrage est un **cours élémentaire de breton** de 1930 organisé en leçons. Chaque leçon contient :

1. **Vocabulaire** : mots en colonnes parallèles breton (gauche) / français (droite)
2. **Grammaire** : règles grammaticales avec exemples, tableaux de mutations
3. **Exercices** : exercices de traduction, d'écriture, de copie
4. **Lectures** (Lennadenn) : textes continus en breton

### Disposition

Les pages sont en vis-à-vis (deux pages par scan). Le vocabulaire est en colonnes parallèles. La grammaire et les exercices sont généralement monolingues ou mixtes.

---

## Règles d'extraction

### Listes de vocabulaire

Les listes de vocabulaire présentent des mots breton ↔ français en colonnes parallèles, souvent sous l'en-tête **GERIOU** (mots). Extrayez chaque paire :
```json
{"breton": "Tad", "français": "Père"}
{"breton": "Mamm", "français": "Mère"}
{"breton": "Breur", "français": "Frère"}
{"breton": "C'hoar", "français": "Sœur"}
```

> Les mots avec articles définis bretons (`an`, `ar`, `al`) ou indéfinis (`ur`, `ul`, `un`) doivent les conserver tels quels quand ils sont présents.

### Dialogues (DIVIZ)

Certaines leçons contiennent des sections **DIVIZ** (Dialogue) structurées en questions-réponses bilingues. Extrayez chaque paire question/réponse :
```json
{"breton": "Petra eo an dra-ze ?", "français": "Qu'est-ce que c'est ?"}
{"breton": "Eun ti eo", "français": "C'est une maison"}
```

> Les DIVIZ sont une source riche de paires bilingues, extrayez tout le contenu.

### Tableaux de mutations

Les tableaux montrant les mutations consonantiques (k → c'h, g → c'h, etc.) sont des contenus **grammaticaux** sans traduction → **exclure**.

Cependant, les tableaux de mutations **avec exemples bilingues** (`va` = mon, `ho` = votre, etc.) doivent être extraits ligne par ligne :
```json
{"breton": "va zad", "français": "mon père"}
{"breton": "ho tad", "français": "votre père"}
```

> Ne confondez pas un **tableau de règles abstraites** (k→g, k→c'h) avec un tableau d'**exemples bilingues** (va zad / mon père).

### Conjugaisons

Les tableaux de conjugaison en deux langues (breton / français en regard) → extraire chaque ligne comme paire quand les deux côtés sont complets :
```json
{"breton": "Me am eus", "français": "J'ai"}
{"breton": "Te az peus", "français": "Tu as"}
```

### Exercices

- **Exercices de traduction** avec des phrases bilingues clairement alignées → **extraire**
- **Exercices à trous** (compléter les mots manquants, écrire en breton) → **exclure**
- **Exercices de copie** (« Skriv en distro ») → **exclure** (monolingue)
- **Exercices numérotés** (« Exercice N° ») : lire le contenu — extraire uniquement si des paires bilingues complètes y figurent

### Lectures (Lennadenn)

Les lectures sont du **texte continu monolingue breton** → **exclure entièrement**. Même si quelques mots français apparaissent, le texte n'est pas bilingue en miroir.

### Résumés (RÉSUMÉ)

Certaines leçons contiennent des pages de **RÉSUMÉ** qui récapitulent le vocabulaire et les expressions de la leçon sous forme de listes bilingues. Extrayez toutes les paires bilingues présentes :
```json
{"breton": "ar gwareg", "français": "la femme"}
{"breton": "ar vugale", "français": "les enfants"}
```

### Sections grammaticales

Les explications de règles sont en français avec des exemples bretons intégrés. Extrayez **uniquement** les exemples clairement présentés comme paires :
```json
{"breton": "Ar gwez", "français": "Les arbres"}
{"breton": "Ar c'hleier", "français": "Les épées"}
```

> Les règles en prose (1re Règle, Renvoi, etc.) → **exclure**.

### Exercices (POELLADENNOU)

- **Exercices numérotés** avec des séries de mots bretons sans traduction (« Lakait ar ger X e-le'h ar ger Y » = « Remplacer le mot X par le mot Y ») → **exclure**
- **Exercices de copie** (« Skriv en distro ») → **exclure** (monolingue)
- **Exercices avec paires bilingues complètes** (traduction française fournie) → **extraire**

### Qualité du scan

Les pages sont nettes. Le texte est en corps standard, bien lisible. Les colonnes de vocabulaire sont clairement alignées.
