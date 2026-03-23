# Rapport d'erreur OCR : geriadur_lexique_1927
**Référence** : `gold/geriadur_lexique_1927/human_reference`
**Hypothèse** : `gold/geriadur_lexique_1927/jsonl`

## Résultats Globaux

- **Breton GLOBAL** : WER: **4,7%**, CER: **2,3%**
- **Français GLOBAL** : WER: **3,8%**, CER: **3,3%**

## Typologie des erreurs

- **Paires référence** : 156
- **Paires hypothèse** : 152
- **Silences** (paires manquantes) : **11** (7,1% des paires référence)
- **Bruit** (paires en trop) : **7** (4,6% des paires hypothèse)

### Analyse qualitative

Les erreurs se concentrent quasi exclusivement sur la page 07 (lettres CI–CÔ). Deux catégories dominent :

1. **Silences (paires manquantes)** — Le modèle omet des entrées présentes dans l'original, souvent parce qu'elles sont fusionnées avec d'autres ou que leur contexte (précisions entre parenthèses) n'est pas restitué. Exemple : `gwadgaser tribrankek (ar c'hof) → tronc coeliaque` est transcrit sans la glose `(ar c'hof)`.

2. **Fautes d'accord** — Le PDF imprimé utilise des abréviations morphologiques : le lemme est donné au masculin singulier, et la forme fléchie est abrégée (ex. « collatérel — artères c. »). Le modèle restitue le mot complet mais ne fait pas l'accord : `artères collatéral` au lieu de `artères collatérales`. Même logique pour `vertèbre cervical` au lieu de `vertèbre cervicale`. Ce type d'erreur est systématique pour les lexiques médicaux qui abrègent l'adjectif.

## Résultats détaillés par page

### 03.jsonl
- **Breton** : WER: 0,0%, CER: 0,0%
- **Français** : WER: 0,0%, CER: 0,0%

### 06.jsonl
- **Breton** : WER: 0,0%, CER: 0,0%
- **Français** : WER: 2,0%, CER: 0,2%

### 07.jsonl
- **Breton** : WER: 15,6%, CER: 8,7%
- **Français** : WER: 10,4%, CER: 10,1%

### 13.jsonl
- **Breton** : WER: 0,0%, CER: 0,0%
- **Français** : WER: 0,0%, CER: 0,0%

### 20.jsonl
- **Breton** : WER: 0,0%, CER: 0,0%
- **Français** : WER: 0,0%, CER: 0,0%
