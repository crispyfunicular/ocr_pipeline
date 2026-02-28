# Instructions spécifiques : Geriadur – Lexique anatomique breton-français (1927)

## Nature de l'ouvrage

Cet ouvrage est un **lexique anatomique et médical** français-breton de 1927. Chaque page contient des **entrées de dictionnaire** dans l'ordre alphabétique, disposées en deux colonnes (pages paires à gauche, impaires à droite). Traitez les deux colonnes séquentiellement.

### Structure d'une entrée

```
mot-vedette — traduction(s) bretonne(s), marque(s).
```

- Le **mot-vedette français** est en gras, suivi d'un tiret `—`
- Les traductions bretonnes suivent, séparées par des virgules quand il y a plusieurs synonymes
- Des **abréviations grammaticales** suivent les mots : `g.` (genre), `gg.` (pluriel), `av.` (adverbe), `nd.` (nom duel), `l.` (locution/pluriel locatif)

### Sous-entrées

Une entrée peut contenir des **sous-entrées** signalées par un terme abrégé en gras renvoyant au mot-vedette. Par exemple :

```
oblique — beskellek — grand o. : kigenn veskellek bras, gg — petit o. : kigenn veskellek bihan, gg.
```

Ici `grand o.` = `grand oblique` et `petit o.` = `petit oblique`. Chaque sous-entrée est une paire distincte.

---

## Règles d'extraction

### Sens de la traduction

> **ATTENTION** : le mot-vedette (en gras) est en **français**, la traduction est en **breton**. Veillez à bien affecter chaque langue au bon champ JSONL.

### Développement des abréviations de renvoi

Les sous-entrées abrègent le mot-vedette parent par **sa première lettre suivie d'un point**. La règle est systématique :

> **Quand vous rencontrez `X.` dans une sous-entrée, remplacez-le par le mot-vedette en gras qui ouvre l'entrée courante.**

Ceci s'applique quelle que soit la position dans l'entrée, y compris quand l'entrée s'étend sur plusieurs lignes ou contient de nombreuses sous-entrées.

Exemples courants :

| Entrée parent | Abréviation lue | Développement correct |
|---|---|---|
| **côlon** | `c. ascendant` | `côlon ascendant` |
| **côlon** | `c. transverse` | `côlon transverse` |
| **côlon** | `c. descendant` | `côlon descendant` |
| **côlon** | `S du c.` | `S du côlon` |
| **cuboïde** | `os c.` | `os cuboïde` |
| **cricoïde** | `cartilage c.` | `cartilage cricoïde` |
| **deltoïde** | `muscle d.` | `muscle deltoïde` |
| **déférent** | `canal d.` | `canal déférent` |
| **dentaire** | `alvéole d.` | `alvéole dentaire` |
| **oblique** | `grand o.` | `grand oblique` |
| **oblique** | `petit o.` | `petit oblique` |
| **obturateur** | `trou o.` | `trou obturateur` |
| **occipital** | `os o.` | `os occipital` |
| **olfactif** | `nerf o.` | `nerf olfactif` |
| **optique** | `nerf o.` | `nerf optique` |
| **orteil** | `gros o.` | `gros orteil` |
| **papille** | `p. du goût` | `papille du goût` |
| **pathétique** | `nerf p.` | `nerf pathétique` |
| **coxo-fémoral** | `articulation c.` | `articulation coxo-fémorale` |
| **visuel** | `acuité v.` | `acuité visuelle` |
| **visuel** | `angle v.` | `angle visuel` |
| **vocal** | `corde v.` | `corde vocale` |
| **voile** | `v. du palais` | `voile du palais` |
| **pituitaire** | `membrane p.` | `membrane pituitaire` |
| **pituitaire** | `glande p.` | `glande pituitaire` |

### Synonymes bretons multiples

Quand une entrée a plusieurs traductions bretonnes séparées par des virgules, **gardez-les toutes dans le même champ breton**. N'éclatez PAS les synonymes.

### Traductions directes vs. gloses descriptives

Certaines entrées contiennent un mot breton direct suivi d'une longue phrase descriptive en breton (description anatomique). Ne gardez que le mot direct — la phrase descriptive n'est pas un synonyme exploitable.

Exemple : `côlon — kolon, g, eil kevrenn ar vou-zellenn deo, gg` → garder uniquement `kolon` (le reste est une glose « deuxième section de l'intestin »).

### Renvois « S. » (synonyme)

Certaines entrées renvoient à un autre mot via `S.` (synonyme). **Ignorez ces entrées** — elles ne contiennent pas de traduction bretonne propre.

Exemple à ignorer : `ombilie — S. nombril.`

### Abréviations grammaticales à supprimer

Supprimez de la sortie : `g.`, `gg.`, `av.`, `nd.`, `l.`, et toute abréviation grammaticale après le mot breton.

### Parenthèses de précision en français

Conservez les précisions entre parenthèses dans le champ français quand elles désambiguïsent le terme :
- `couche (graisseuse, etc.)` ✅
- `creux (de la main)` ✅
- `détroit (du bassin)` ✅
- `oreillette (du cœur)` ✅
- `ventricule (du cœur)` ✅
- `pavillon (de l'oreille)` ✅
- `poil (du corps)` ✅
- `plante (du pied)` ✅
- `plancher (de la bouche)` ✅

### Formes dérivées avec tiret-préfixe

Quand une variante bretonne est indiquée par un tiret-préfixe seul (ex : `-kilpenn` sous `kilpennel`), cela indique une racine ou un suffixe — **ignorez ces fragments**. Gardez uniquement les formes complètes et autonomes.

### Entrées composées avec plusieurs sous-entrées en ligne

Certaines entrées contiennent l'adjectif principal suivi de plusieurs sous-entrées sur les lignes suivantes, chacune avec un qualificatif en gras. Par exemple :

```
visuel — ar gweled — acuité v. : lemm-der-gweled — angle v. : kornad-gweled
```

Extrayez :
1. L'entrée principale : `{"breton": "ar gweled", "français": "visuel"}`
2. Chaque sous-entrée avec le terme développé

### Tiret composé (trait d'union long)

Certains mots bretons composés utilisent un tiret long (`-ha-`, `-ar-`). Conservez-les tels quels :
- `skevent-ha-kreuz` → garder intégralement
- `skevent-ha-sac'h-boued` → garder intégralement

---

## Exemples complets

Voici comment extraire des entrées typiques de ce lexique :

### Entrée simple
Image : `cou — gouzoug, g.`
```json
{"breton": "gouzoug", "français": "cou"}
```

### Entrée avec précision contextuelle et synonymes
Image : `couche — (graisseuse, etc.) gwiskad, g, gwelead, g.`
```json
{"breton": "gwiskad, gwelead", "français": "couche (graisseuse)"}
```

### Entrée avec sous-entrées abrégées
Image : `oblique — beskellek — grand o. : kigenn veskellek bras, gg — petit o. : kigenn veskellek bihan, gg.`
```json
{"breton": "beskellek", "français": "oblique"}
{"breton": "kigenn veskellek bras", "français": "grand oblique"}
{"breton": "kigenn veskellek bihan", "français": "petit oblique"}
```

### Entrée avec une seule sous-entrée
Image : `déférent — diskarg — canal d. : kansper, g.`
```json
{"breton": "diskarg", "français": "déférent"}
{"breton": "kansper", "français": "canal déférent"}
```

### Entrée longue avec nombreuses sous-entrées (côlon)
Image : `côlon — kolon, g, eil kevrenn ar vou-zellenn deo, gg — c. ascendant : bann-sevel ar c'holon, g. — c. transverse : treuzell ar c'holon, gg — c. descendant : bann-diskenn ar c'holon, g. — S du c. : S ar c'holon, g.`

> Le mot-vedette est `côlon`. Toute occurrence de `c.` dans les sous-entrées doit être développée en `côlon` :
```json
{"breton": "kolon", "français": "côlon"}
{"breton": "bann-sevel ar c'holon", "français": "côlon ascendant"}
{"breton": "treuzell ar c'holon", "français": "côlon transverse"}
{"breton": "bann-diskenn ar c'holon", "français": "côlon descendant"}
{"breton": "S ar c'holon", "français": "S du côlon"}
```

### Entrée avec nom duel
Image : `œil — lagad, g, nd. daoulagad.`
```json
{"breton": "lagad", "français": "œil"}
```

### Entrée avec locution pluriel
Image : `organe — benveg, g, l. binviou, benvegenn, gg.`
```json
{"breton": "benveg, binviou, benvegenn", "français": "organe"}
```

### Entrée renvoi (à ignorer)
Image : `ombilie — S. nombril.`
→ **Ne pas extraire** (renvoi synonymique, pas de traduction)

### Entrée avec qualificatif de sous-type

Image : `pectoral — -brennid — grand p. : kigenn-vrennid vras, gg — petit p. : kigenn-vrennid vihan, gg.`

> Le mot-vedette `pectoral` n'a qu'un fragment breton (`-brennid`) — **ignorez l'entrée principale** (fragment inutilisable). Extrayez uniquement les sous-entrées complètes :
```json
{"breton": "kigenn-vrennid vras", "français": "grand pectoral"}
{"breton": "kigenn-vrennid vihan", "français": "petit pectoral"}
```

### Entrée avec locution composée

Image : `vocal — mouezel, -mouez — corde v. : korden-vouez, l. kerdin-mouez.`

> Gardez le mot complet (`mouezel`), **supprimez le fragment** (`-mouez`) :
```json
{"breton": "mouezel", "français": "vocal"}
{"breton": "korden-vouez, kerdin-mouez", "français": "corde vocale"}
```

### Fin du dictionnaire

La dernière page se termine par un trait décoratif (`——w——`). **Ignorez** ces marques de fin de section.

### Qualité du scan

Ce lexique de 1927 est globalement bien imprimé. Les caractères sont nets dans la grande majorité des cas. La jointure centrale peut affecter quelques mots — ignorez uniquement ceux qui sont réellement illisibles.
