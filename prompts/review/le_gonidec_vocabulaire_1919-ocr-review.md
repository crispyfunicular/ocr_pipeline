# Critères de révision spécifiques : Le Gonidec — Vocabulaire (1919)

## Nature de l'ouvrage

Dictionnaire français-breton complet (~300 pages, 35 000+ paires). Alphabétique A–Z avec un Supplément (errata/additions). Deux colonnes par page (pages gauche et droite d'un même scan).

## Vérifications spécifiques

### Résolution des tirets cadratins (`—`)

Le dictionnaire utilise le tiret cadratin pour remplacer le mot vedette dans les sous-entrées. C'est la règle la plus critique pour ce livre.

**Vérifier** :
- [ ] **Aucun tiret cadratin** ne subsiste dans les champs `français`
- [ ] Les tirets sont résolus correctement avec le mot vedette (ex : sous `baryton`, `voix de —` → `voix de baryton`)
- [ ] Les sous-entrées avec locutions sont correctement formées (ex : `(pain) qui a une —` sous `baisure` → `pain qui a une baisure`)

### Verbes pronominaux

Les verbes notés `verbe (s')` dans le dictionnaire doivent être normalisés.

**Vérifier** :
- [ ] La forme pronominale est normalisée (ex : `accouder (s')` → `s'accouder`)
- [ ] Les deux formes (active et pronominale) sont des paires distinctes quand les traductions diffèrent

### Liste des 28 abréviations

Le prompt livre liste 28 abréviations à supprimer (m., f., pl., adj., Van., Trég., U.B., etc.).

**Vérifier** :
- [ ] Aucune abréviation de la liste n'apparaît dans les champs extraits
- [ ] Les abréviations dans le **contexte français** (ex : `complément de subst. ou d'adj.`) sont acceptables — elles font partie de la définition, pas du formatage du dictionnaire

### Notes grammaticales bretonnes dans le champ français

Le dictionnaire indique parfois la préposition, le pluriel, le collectif ou la variante dialectale du mot breton. Ces notes **ne doivent pas** figurer dans le champ `français`.

**Vérifier** :
- [ ] Aucune préposition bretonne (ex : `ouz`, `da`, `gant`) dans le champ `français`
- [ ] Aucun pluriel breton (ex : `pl. tud`, `pl. -zidi`) dans le champ `français`
- [ ] Aucune variante dialectale (ex : `Van. arouarek`, `Trég. ...`) dans le champ `français`

### Première lettre tronquée

La marge gauche peut couper la première lettre de certaines vedettes. Le prompt autorise la reconstruction à partir de la lettre de section alphabétique.

**Vérifier** :
- [ ] Les vedettes reconstruites sont cohérentes avec la section alphabétique
- [ ] Aucune vedette ne commence par un caractère incohérent (ex : lettre `A` avec vedette commençant par `B`)

### Supplément / Errata

Les dernières pages (pp. 590+) contiennent des corrections et additions éditoriales. Le contenu est un mélange de vocabulaire extractible et de commentaires éditoriaux non extractibles.

**Vérifier** :
- [ ] Seul le vocabulaire extractible est capturé (corrections `Corriger: X` et ajouts `Ajouter: Y`)
- [ ] Les commentaires éditoriaux, essais phonétiques et notes ne sont pas extraits

### Extractions croisées et synonymes

Le dictionnaire donne souvent plusieurs traductions bretonnes pour un même mot français, séparées par des virgules.

**Vérifier** :
- [ ] Chaque synonyme breton est une paire distincte (ex : `étrenne → kalanna` et `étrenne → derou-mat`)
- [ ] Le nombre de paires par page est cohérent avec la densité visuelle du dictionnaire

### Continuations de page

La première entrée d'une colonne peut être la continuation d'une entrée de la page précédente.

**Vérifier** :
- [ ] Les textes de continuation (sans vedette propre) sont correctement exclus ou gérés selon le contexte
- [ ] Les sous-locutions dans les continuations sont extraites si elles constituent des paires autonomes
