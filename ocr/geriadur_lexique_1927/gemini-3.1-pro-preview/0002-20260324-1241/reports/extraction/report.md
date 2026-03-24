# Rapport d'extraction du corpus bilingue

> Généré automatiquement par `src/ocr`
> Dernière mise à jour : 2026-03-24 19:19
> Livre : `geriadur_lexique_1927`
> Modèle : `gemini-3.1-pro-preview`

## Synthèse globale

- **Pages traitées** : 18 / 22
- **Paires extraites** : 716 (39.8 /page)
- **OK** : 14 — **Difficultés** : 0 — **Impossible** : 4
- **Score** : moy 78% · min 0% · max 100%
- **Temps** : 11.9 min (39.7s /page)
- **Coût** : $0.5193 ($0.0289 /page)

## Rapport détaillé

| Image | Paires | Statut | Score | Temps | Coût | Remarques |
|-------|-------:|--------|------:|------:|-----:|----------|
| `01.jpg` | 0 | Impossible | 0%% | 6.3s | $0.0189 | Page de titre, aucun contenu bilingue à extraire. |
| `02.jpg` | 0 | Impossible | 0%% | 8.4s | $0.0189 | Page de titre ne contenant aucune paire bilingue exploitable. |
| `04.png` | 56 | OK | 100%%% | 59.4s | $0.0324 | Page très lisible, les règles de développement des abréviations et de suppression des fragments ont été appliquées avec succès. |
| `05.jpg` | 48 | OK | 100%% | 52.6s | $0.0314 | Extraction propre, les abréviations ont été développées (avec accord grammatical en français quand nécessaire, ex: cavité buccale) et les gloses descriptives longues ont été ignorées conformément aux règles. |
| `08.jpg` | 50 | OK | 100%% | 47.6s | $0.0318 | Page très nette, extraction des entrées et sous-entrées en appliquant les règles de rejet des fragments (ex: -diskarg, -morzed) et des abréviations grammaticales (nd., l.). |
| `09.jpg` | 52 | OK | 100%% | 48.5s | $0.0315 | Scan de bonne qualité, extraction des entrées et sous-entrées en appliquant les règles de nettoyage (parenthèses, fragments, gloses longues). |
| `10.jpg` | 58 | OK | 100%% | 45.3s | $0.0325 | Extraction sans difficulté majeure, les règles d'exclusion des fragments (tiret initial) et de développement des abréviations avec accord (ex: matières fécales) ont été appliquées. |
| `11.jpg` | 47 | OK | 100%% | 59.5s | $0.0306 | Page très lisible, extraction sans difficulté majeure en appliquant les règles de filtrage des fragments et des abréviations. |
| `12.jpg` | 58 | OK | 100%% | 52.2s | $0.0333 | Extraction réussie. Les mots coupés en fin de ligne (ex: dives-ker, diougar-van, in-férieure, beg-as-kourn, klopenvron-nenn) ont été recollés. La mention entre parenthèses "(-askourn)" a été supprimée comme demandé par les règles générales. |
| `13.png` | 54 | OK | 100%%%% | 51.3s | $0.0321 | Extraction propre, les règles de développement des abréviations avec accord de genre (ex: fosse nasale, paire nerveuse) et d'exclusion des fragments (ex: -kreiz, -mel) ont été appliquées avec succès. |
| `14.jpg` | 54 | OK | 100% | 55.6s | $0.0320 | L'entrée "nerf pathétique" a été ignorée car sa traduction bretonne dépasse 3 mots. |
| `15.jpg` | 52 | OK | 100% | 36.0s | $0.0323 | Page très lisible, extraction des sous-entrées et synonymes effectuée selon les règles, fragments et renvois ignorés. |
| `16.jpg` | 44 | OK | 100% | 28.6s | $0.0300 | Extraction réussie, application stricte des règles concernant les fragments (ignorés), les segments de plus de 3 mots (ignorés), et le développement des abréviations. |
| `17.jpg` | 52 | OK | 100% | 45.2s | $0.0319 | Extraction sans difficulté majeure, application des règles d'accord grammatical pour les abréviations développées en français (ex: glandes salivaires, vésicule séminale). |
| `18.jpg` | 42 | OK | 100% | 56.4s | $0.0304 | Extraction complète et conforme aux règles, les fragments et renvois ont été ignorés, et les abréviations développées. |
| `19.jpg` | 49 | OK | 100% | 51.7s | $0.0314 | Page très nette, les règles concernant les fragments (ex: -troaz), les renvois (S. poitrine) et le développement des abréviations avec accord grammatical (fonctions végétatives) ont été appliquées avec succès. |
| `21.jpg` | 0 | Impossible | 0% | 5.2s | $0.0190 | Page d'informations d'édition (imprimerie, date), aucun contenu bilingue à extraire. |
| `22.jpg` | 0 | Impossible | 0% | 4.1s | $0.0189 | L'image ne contient aucun texte, seulement une ligne noire sur fond blanc. |
