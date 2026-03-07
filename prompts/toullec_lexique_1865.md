# Instructions spécifiques : Toullec – Lexique français-breton (1865)

## Nature de l'ouvrage

Cet ouvrage est un **lexique bilingue** breton-français de 1865. Il contient :

- Une **préface/avertissement** en deux colonnes parallèles (breton à gauche « KELENNADUREZ », français à droite « AVERTISSEMENT ») — du texte continu à extraire phrase par phrase
- Des **listes de vocabulaire** organisées par thème, avec des entrées breton/français en colonnes
- Des **sections grammaticales** avec exemples bilingues

## Consignes d'extraction renforcées

> **Ce lexique est globalement bien imprimé et lisible.** Ne rejetez PAS des pages entières comme « trop floues ». La grande majorité du texte est parfaitement déchiffrable. Extrayez tout ce que vous pouvez lire.

### Préface en colonnes parallèles
Les pages de préface présentent du texte continu breton (gauche) / français (droite). Alignez phrase par phrase en découpant au niveau des points. Ces paragraphes sont des traductions complètes l'un de l'autre.

### Entrées lexicales
- Chaque entrée contient un mot breton et sa traduction française
- **Supprimez** systématiquement : les marques de genre (f., m., c.), les abréviations grammaticales (adj., v., s., pl.), les numéros d'ordre
- **Supprimez** les variantes entre parenthèses sauf si elles constituent un mot distinct utile (ex : `Anet (d'an holl)` → `Anet`, `Moreau (cheval)` → `Moreau`)
- **Supprimez** les annotations en italique après le mot principal (ex : `Kintuz, grignoux` → `Kintuz`, `Kruel digaloun` → `Kruel`)
- Quand une entrée a plusieurs traductions séparées par des virgules, créez **une paire JSONL par traduction**. Exemple : `Eur persoun — Un recteur, un desservant` → `{"breton": "Eur persoun", "français": "Un recteur"}` + `{"breton": "Eur persoun", "français": "un desservant"}`
- Extrayez chaque entrée comme une paire indépendante

### Suffixes de genre (adjectifs)
Les pages d'adjectifs utilisent des tirets pour indiquer la forme féminine : `Obligeant—e`, `Grand—de`, `Court—te`, `Peureux—se`. **Gardez uniquement la forme masculine** (sans le suffixe féminin) : `Obligeant`, `Grand`, `Court`, `Peureux`.

### Disposition en 4 colonnes
Certaines pages (vocabulaire, adjectifs) présentent **4 colonnes** : BR1, FR1, BR2, FR2. Traitez chaque paire (BR1/FR1) et (BR2/FR2) indépendamment. Ne mélangez pas les colonnes gauche et droite.

### Accolades (regroupements avec `{`)
Certaines entrées utilisent une **accolade** pour regrouper plusieurs sous-entrées sous un mot commun. Alignez **ligne par ligne** les sous-entrées bretonne et française, en préfixant chacune avec le mot commun. Exemple :
```
Bara { fresk       Du pain { frais
      { diasez               rassis
      { loued                 moisi
```
Produit :
```json
{"breton": "Bara fresk", "français": "Du pain frais"}
{"breton": "Bara diasez", "français": "Du pain rassis"}
{"breton": "Bara loued", "français": "Du pain moisi"}
```
Autre exemple :
```
Eun akt { a feiz         Un acte { de foi
         { a esperans             d'espérance
         { a garantez             de charité
         { a adoration            d'adoration
         { a gontrision           de contrition
```
Produit :
```json
{"breton": "Eun akt a feiz", "français": "Un acte de foi"}
{"breton": "Eun akt a esperans", "français": "Un acte d'espérance"}
{"breton": "Eun akt a garantez", "français": "Un acte de charité"}
{"breton": "Eun akt a adoration", "français": "Un acte d'adoration"}
{"breton": "Eun akt a gontrision", "français": "Un acte de contrition"}
```

### Qualité du scan
Ce lexique de 1865 a un texte petit mais net. Les caractères sont lisibles dans la très grande majorité des cas. Ne laissez pas la taille de la police vous décourager — si vous pouvez lire le mot, extrayez-le.

### Phrases tronquées en fin de page
La préface est découpée sur plusieurs pages. Quand une phrase est coupée par la fin de la colonne (césure, mot incomplet), **rejetez-la entièrement**. Chaque paire extraite doit faire sens des deux côtés.

Exemple à **NE PAS** extraire :
```json
{"breton": "Bras e ve abaff ho c'herend pa lakeont e tre daquarn ho bugale pere a gredont desket mad, eur skrit, euz lizer-ferm pe eur c'hountrat all benag pehini o tendues", "français": "Ces jeunes gens sont cependant convaincus qu'ils sont instruits jusqu'à ce que la mise en pratique de leurs pré-"}
```
↑ La phrase française est coupée (« pré- ») → rejeter.
