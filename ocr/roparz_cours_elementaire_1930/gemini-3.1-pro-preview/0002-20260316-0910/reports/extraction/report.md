# Rapport d'extraction du corpus bilingue

> Généré automatiquement par `src/ocr`
> Dernière mise à jour : 2026-03-16 10:26
> Livre : `roparz_cours_elementaire_1930`
> Modèle : `gemini-3.1-pro-preview`

## Synthèse globale

- **Pages traitées** : 21 / 21
- **Paires extraites** : 653 (31.1 /page)
- **OK** : 21 — **Difficultés** : 0 — **Impossible** : 0
- **Score** : moy 100% · min 100% · max 100%
- **Temps** : 15.4 min (44.0s /page)
- **Coût** : $0.5139 ($0.0245 /page)

## Rapport détaillé

| Image | Paires | Statut | Score | Temps | Coût | Remarques |
|-------|-------:|--------|------:|------:|-----:|----------|
| `04.jpg` | 21 | OK | 100% | 41.8s | $0.0215 | Extraction du vocabulaire avec application des règles de mutation, et d'une phrase de dialogue (les marqueurs de rôle non en gras ont été ignorés). |
| `05.jpg` | 17 | OK | 100% | 36.6s | $0.0205 | Page de gauche ignorée car constituée d'exercices à trous avec ellipses ; mots grammaticaux isolés en fin de liste de vocabulaire ignorés selon les consignes ; mutations appliquées correctement. |
| `06.jpg` | 40 | OK | 100% | 43.7s | $0.0260 | Extraction propre des sections DIVIZ et GERIOU avec application stricte des règles de mutation (d-taol -> daol, c'h-kelenner -> c'helenner, etc.) et nettoyage des préfixes/parenthèses. |
| `07.jpg` | 21 | OK | 100% | 24.6s | $0.0229 | Extraction réussie, les règles de mutation (c'h-kreion -> c'hreion, g-kador -> gador, n-dor -> nor) ont été appliquées et les préfixes de dialogue supprimés. |
| `08.jpg` | 43 | OK | 100% | 35.8s | $0.0268 | Extraction propre du vocabulaire et des dialogues, application stricte des règles de mutation (g-kambr -> gambr, v-boest -> voest, g-kleuzeur -> gleuzeur) et suppression des parenthèses et préfixes de dialogue. |
| `09.jpg` | 29 | OK | 100% | 51.0s | $0.0232 | Extraction du vocabulaire de la leçon 5, application des règles de mutation et exclusion des prépositions isolées. |
| `10.jpg` | 11 | OK | 100% | 39.9s | $0.0209 | Extraction de la section DIVIZ avec application stricte des règles de mutation (d-taol -> daol, n-dor -> nor, d-tra -> dra) et suppression des préfixes de dialogue. Quelques exemples traduits ont été extraits des sections POELLADENNOU et NOTENNOU. La page de droite (17) a été ignorée car elle ne contient pas de paires bilingues alignées. |
| `12.jpg` | 44 | OK | 100% | 36.5s | $0.0276 | Extraction propre du vocabulaire et des dialogues ; les mutations ont été appliquées (ex: w-gwe-lit -> welit, v-brao -> vrao) et les sections monolingues (Lennadenn, Poelladennou) ont été ignorées conformément aux instructions. |
| `13.jpg` | 35 | OK | 100% | 53.7s | $0.0252 | Extraction des exemples grammaticaux, du vocabulaire (avec application des mutations et exclusion des mots-outils isolés comme e-pad, na, hogen) et des phrases de dialogue (sans les annotations littérales). |
| `14.jpg` | 10 | OK | 100% | 30.1s | $0.0203 | Extraction des dialogues de la section DIVIZ avec application des mutations et suppression des préfixes ; les sections LENNADENN, POELLADENNOU et NOTENNOU ont été ignorées car monolingues ou contenant des traductions intercalées dans le texte français. |
| `15.jpg` | 43 | OK | 100% | 48.4s | $0.0268 | Extraction du vocabulaire et des phrases de dialogue avec application des règles de mutation et nettoyage des préfixes/parenthèses. |
| `16.jpg` | 28 | OK | 100% | 62.0s | $0.0231 | Extraction du vocabulaire et des phrases de dialogue avec application des règles de mutation (w-gwinterell -> winterell, d-tra -> dra, z-diskouez -> ziskouez) et exclusion des pronoms/prépositions isolés. |
| `18.jpg` | 34 | OK | 100% | 38.6s | $0.0255 | Extraction du vocabulaire et des dialogues avec application stricte des règles de mutation (ex: c'h-kazarc'h -> c'hazarc'h, v-miz -> viz) et suppression des préfixes et parenthèses. |
| `20.jpg` | 40 | OK | 100% | 50.5s | $0.0262 | Extraction des exemples grammaticaux, du vocabulaire et des dialogues avec application stricte des règles de mutation, suppression des préfixes/parenthèses et exclusion des mots purement grammaticaux ("da" / "pour") et des traductions incomplètes ("ho p-brec'h" / "votre"). |
| `21.jpg` | 12 | OK | 100% | 33.8s | $0.0198 | Extraction des dialogues (avec application des mutations et suppression des préfixes/parenthèses), du vocabulaire en bas de page et des formes verbales isolées ; exclusion des exercices et textes monolingues. |
| `22.jpg` | 54 | OK | 100% | 39.8s | $0.0305 | Extraction propre du vocabulaire et des dialogues avec application stricte des règles de mutation (v-maouez -> vaouez, b-poan -> boan, v-bloaz -> vloaz, p-bleo -> pleo) et découpage des phrases multiples. |
| `23.jpg` | 34 | OK | 100% | 49.5s | $0.0246 | Extraction du vocabulaire avec application des règles de mutation et suppression des mots grammaticaux isolés. Les parenthèses dans les exemples grammaticaux ont été supprimées avec leur contenu pour isoler les formes verbales. |
| `24.jpg` | 39 | OK | 100% | 50.0s | $0.0273 | Extraction propre des dialogues (DIVIZ) et de la liste de vocabulaire (pluriels), avec application stricte des règles de mutation et suppression des parenthèses explicatives. |
| `25.jpg` | 40 | OK | 100% | 64.1s | $0.0270 | Extraction du vocabulaire, des dialogues et des exemples d'exercices avec application stricte des règles de mutation et exclusion des mots grammaticaux isolés. |
| `26.jpg` | 40 | OK | 100% | 47.4s | $0.0259 | Extraction des listes de vocabulaire et des dialogues avec application stricte des règles de mutation orthographique. |
| `27.jpg` | 18 | OK | 100% | 47.1s | $0.0223 | Extraction des dialogues (sans préfixes ni parenthèses) et des tableaux de conjugaison ; exclusion des sections monolingues (Lennadenn, Poelladennou, Notennou). |
