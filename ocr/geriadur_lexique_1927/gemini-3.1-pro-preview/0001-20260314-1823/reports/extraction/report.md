# Rapport d'extraction du corpus bilingue

> Généré automatiquement par `scripts/ocr`
> Dernière mise à jour : 2026-03-14 23:14
> Livre : `geriadur_lexique_1927`
> Modèle : `gemini-3.1-pro-preview`

## Synthèse globale

- **Pages traitées** : 18 / 18
- **Paires extraites** : 649 (36.1 /page)
- **OK** : 18 — **Difficultés** : 0 — **Impossible** : 0
- **Score** : moy 100% · min 100% · max 100%
- **Temps** : 13.1 min (43.6s /page)
- **Coût** : $0.5166 ($0.0287 /page)

## Rapport détaillé

| Image | Paires | Statut | Score | Temps | Coût | Remarques |
|-------|-------:|--------|------:|------:|-----:|----------|
| `03.jpg` | 12 | OK | 100% | 26.4s | $0.0220 | Page d'introduction avec liste d'abréviations ignorée comme demandé, extraction des premières entrées du dictionnaire. |
| `04.jpg` | 36 | OK | 100% | 49.3s | $0.0289 | Extraction sans difficulté majeure, les règles spécifiques au lexique ont été appliquées (développement des abréviations, suppression des fragments avec tiret, gestion des parenthèses de désambiguïsation). |
| `05.jpg` | 40 | OK | 100% | 52.3s | $0.0298 | Les règles spécifiques au lexique ont été appliquées avec succès, notamment le développement des abréviations, la suppression des fragments avec tiret et l'exclusion des descriptions longues. |
| `06.jpg` | 38 | OK | 100% | 43.8s | $0.0295 | Extraction sans problème majeur ; l'erreur typographique (parenthèse non fermée) sous "cervical" a été gérée en supprimant le contenu parentothétique conformément aux règles, et les abréviations grammaticales ("as", "l.", etc.) ont été correctement filtrées. |
| `07.jpg` | 34 | OK | 100%% | 43.7s | $0.0291 | Extraction propre, application stricte de la règle des 3 mots maximum pour le breton (exclusion des sous-entrées "corde du tympan" et "apophyse coronoïde du maxillaire inférieur" dont les traductions dépassaient cette limite). |
| `08.jpg` | 41 | OK | 100%% | 41.5s | $0.0297 | Extraction sans difficulté majeure, application stricte des règles de développement des abréviations et d'exclusion des fragments. |
| `09.jpg` | 39 | OK | 100% | 36.6s | $0.0293 | Extraction fluide, application stricte des règles d'exclusion pour les fragments (ex: "-kas"), les gloses de plus de 3 mots (ex: pour "duodénum") et les renvois synonymiques. |
| `10.jpg` | 40 | OK | 100% | 42.1s | $0.0294 | Extraction fluide, les mots coupés en fin de ligne ont été recollés (ex: astennerez, kigenn-blega) et les abréviations développées avec l'accord grammatical approprié (ex: matières fécales). |
| `11.jpg` | 37 | OK | 100% | 37.4s | $0.0289 | Page très nette, application stricte des règles d'exclusion des fragments (ex: iliaque, inférieur, interne) et des gloses descriptives (ex: iléon, hématine). |
| `12.jpg` | 36 | OK | 100% | 34.7s | $0.0290 | Page très propre, les règles de suppression des fragments (ex: -tu, -gouzoug) et de développement des abréviations ont été appliquées avec succès, ainsi que la recombinaison des mots coupés en fin de ligne. |
| `13.jpg` | 44 | OK | 100%% | 36.3s | $0.0302 | Extraction propre, les fragments préfixés par un tiret ont été ignorés et les abréviations de sous-entrées ont été développées en accordant le genre en français (ex: fosse nasale, paire nerveuse). |
| `14.jpg` | 41 | OK | 100%% | 47.2s | $0.0297 | Extraction sans difficulté majeure, application stricte des règles de filtrage (rejet de la sous-entrée "nerf pathétique" car > 3 mots). |
| `15.jpg` | 38 | OK | 100% | 34.0s | $0.0297 | Extraction sans difficulté, les règles spécifiques au lexique ont été appliquées (développement des abréviations, suppression des fragments avec tiret, gestion des synonymes). |
| `16.jpg` | 37 | OK | 100% | 84.0s | $0.0286 | Page très nette, application stricte des règles d'exclusion des fragments, des gloses longues (ex: "lost ar vouzellenn deo") et des renvois synonymiques. |
| `17.jpg` | 41 | OK | 100% | 41.4s | $0.0297 | Extraction sans difficulté majeure, les règles de développement des abréviations et de filtrage des fragments ont été appliquées. |
| `18.jpg` | 32 | OK | 100% | 45.5s | $0.0283 | Extraction sans difficulté majeure, application stricte des règles de filtrage (fragments, renvois, segments de plus de 3 mots). |
| `19.jpg` | 39 | OK | 100% | 61.0s | $0.0292 | Extraction propre, les abréviations ont été développées et les segments de plus de 3 mots (comme pour "végétatif") ont été ignorés conformément aux instructions. |
| `20.jpg` | 24 | OK | 100%% | 26.8s | $0.0256 | Extraction sans difficulté, les règles spécifiques au lexique ont été appliquées (développement des abréviations, suppression des fragments, gestion des synonymes). |
