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

### Lexique (I. - GERIOU)

Pour chaque leçon (Kentel), extrayez le lexique situé sous l'en-tête **I. - GERIOU**.
Le mot breton se trouve dans la colonne de gauche et sa traduction française dans la colonne de droite. Extrayez chaque paire :
```json
{"breton": "ar c'h-kelenner", "français": "le professeur"}
{"breton": "an diskibl", "français": "l'élève"}
```

> Les mots avec articles définis bretons (`an`, `ar`, `al`) ou indéfinis (`ur`, `ul`, `un`) doivent les conserver tels quels quand ils sont présents.

> **TRÈS IMPORTANT — Mutations consonantiques :** Dans cet ouvrage, les mutations sont imprimées avec la nouvelle consonne mutée suivie d'un trait d'union puis du mot racine (ex : `d-taol`, `g-kador`, `n-dor`, `b-pluenn`, `v-boest`).
> Vous devez écrire le mot muté correctement en **remplaçant la première lettre (ou le groupe comme gw, k) de la racine par la ou les lettres situées avant le trait d'union**. Le trait d'union disparaît.
> Exemples :
> - `d-taol` → `daol` (et non dtaol)
> - `g-kador` → `gador` (et non gkador)
> - `g-kambr` → `gambr`
> - `v-boest` → `voest`
> - `n-dor` → `nor` (et non ndor)
> - `b-pluenn` → `bluenn`
> - `c'h-kreion` → `c'hreion` (et non c'hkreion)
> - `v-moger` → `voger`
> - `c'h-krog` → `c'hrog`
> - `w-gwerenn` → `werenn`
> - `c'h-goumenn` → `c'houmenn` (et non c'hgoumenn)
> - `c'h-korn-liou` → `c'horn-liou` (et non c'hkorn-liou)
>
> Ceci s'applique partout (GERIOU et DIVIZ).


### Phrases traduites (II. - DIVIZ)

Pour chaque leçon, extrayez les phrases traduites situées sous l'en-tête **II. - DIVIZ**. 
Le breton se trouve à gauche **en gras**, et le français se trouve à la suite ou à droite, **entre parenthèses**.

- **Les parenthèses ne doivent pas être conservées** dans les textes extraits.
- **Les phrases tronquées doivent être ignorées** (par ex. si la phrase continue sur la page suivante).
- **NE CONSERVEZ PAS les chiffres et/ou initiales dans les dialogues**. Supprimez systématiquement les préfixes comme "1.", "2.", "G.", "R.", etc., au début des phrases (aussi bien en breton qu'en français).

Exemple d'extraction (sans les préfixes) :
```json
{"breton": "Petra a ran ?", "français": "Qu'est-ce que je fais ?"}
{"breton": "Skriva a rit", "français": "Vous écrivez."}
```

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

### En-têtes de leçon (KENTEL / LEÇON)

Les en-têtes de leçon (`KENTEL 3 [LEÇON 3]`, `KENTEL 12 [LEÇON 12]`, etc.) sont des marqueurs structurels, pas du vocabulaire → **exclure**. Ne les extrayez pas comme paires bilingues.

### Qualité du scan

Les pages sont nettes. Le texte est en corps standard, bien lisible. Les colonnes de vocabulaire sont clairement alignées.
