# Instructions spécifiques : Colloque français et breton (1890)

## Nature de l'ouvrage

Cet ouvrage est un **colloque bilingue** (phrasebook) de 1890 qui contient :

- Des **listes de vocabulaire par thème** organisées en 4 colonnes (BR1 | FR1 | BR2 | FR2)
- Des **dialogues conversationnels** avec phrases parallèles français ↔ breton en 4 colonnes
- Des **listes de verbes** (« Des Verbes les plus nécessaires ») en colonnes parallèles

### Disposition typique

L'en-tête de chaque double page indique « COLLOQUE » (gauche) et « FRANÇAIS ET BRETON » (droite). Les pages sont numérotées en haut.

---

## Règles d'extraction

### Listes de vocabulaire en 4 colonnes

Les pages de vocabulaire présentent 4 colonnes :
- Colonnes 1-2 : mot breton | traduction française
- Colonnes 3-4 : mot breton | traduction française

**Traitez chaque paire (colonne 1/2) et (colonne 3/4) indépendamment.** Ne mélangez jamais les colonnes gauche et droite.

```json
{"breton": "Displega", "français": "Expliquer, Déployer"}
{"breton": "Dizouna", "français": "Sevrer"}
{"breton": "Eva", "français": "Boire"}
{"breton": "Kuitaat", "français": "Quitter"}
{"breton": "Klask, Enklask", "français": "Chercher"}
```

### Synonymes avec « ou »

Quand un mot breton ou français présente des variantes avec « ou » ou « , » (virgule), créez une entrée distincte pour chaque variante :

```json
{"breton": "Bale", "français": "Marcher"}
{"breton": "Querzet", "français": "Marcher"}
{"breton": "Goada", "français": "Saigner"}
{"breton": "Dic'hoada", "français": "Saigner"}
```

### Dialogues conversationnels

Les pages de dialogue présentent des phrases parallèles en 4 colonnes :
- Colonne 1 : phrase française
- Colonne 2 : traduction bretonne
- Colonne 3 : phrase française (suite)
- Colonne 4 : traduction bretonne (suite)

Extrayez chaque paire de phrases indépendamment :
```json
{"breton": "Bez' em beuz e ker eunn ti a zo leun a varc'hadourez.", "français": "J'ai en ville une maison qui est remplie de marchandises."}
{"breton": "Mont a rinn.", "français": "Je n'y manquerai pas."}
```


### Titres de sections thématiques

Les titres de catégories sont parfois bilingues ou en français seul. **Ignorez les titres purement organisationnels** (comme « Des Verbes les plus nécessaires du 1er ordre ») — ce sont des métadonnées, pas des unités sémantiques.

Extrayez un titre **uniquement** s'il constitue une vraie paire lexicale utile, par exemple un titre de profession bilingue :
```json
{"breton": "Eur C'harr", "français": "Une Charrette"}
```

### Sections à exclure

- Les en-têtes de page « COLLOQUE » / « FRANÇAIS ET BRETON » ne sont pas des paires utiles → **exclure**
- Les numéros de page → **exclure**

### Qualité du scan

Le texte est en caractères petits mais généralement nets. Les colonnes sont bien séparées par des espaces ou des traits verticaux. La jointure centrale peut affecter quelques mots — ignorez-les si illisibles.
