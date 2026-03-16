# Rapport d'extraction du corpus bilingue

> Généré automatiquement par `scripts/ocr`
> Dernière mise à jour : 2026-03-14 19:40
> Livre : `roparz_cours_elementaire_1930`
> Modèle : `gemini-3.1-pro-preview`

## Synthèse globale

- **Pages traitées** : 5 / 31
- **Paires extraites** : 151 (30.2 /page)
- **OK** : 4 — **Difficultés** : 0 — **Impossible** : 1
- **Score** : moy 80% · min 0% · max 100%
- **Temps** : 3.2 min (38.3s /page)
- **Coût** : $0.1206 ($0.0241 /page)

## Rapport détaillé

| Image | Paires | Statut | Score | Temps | Coût | Remarques |
|-------|-------:|--------|------:|------:|-----:|----------|
| `02.jpg` | 0 | Impossible | 0% | 5.2s | $0.0160 | Page de titre ne contenant aucun texte bilingue parallèle. |
| `06.jpg` | 33 | OK | 100% | 48.9s | $0.0247 | Extraction des dialogues (DIVIZ) avec suppression des préfixes et parenthèses, application stricte des règles de mutation (ex: d-taol -> daol, c'h-kelenner -> c'helenner), et exclusion des prépositions/pronoms de la liste de vocabulaire selon les consignes sur les mots-outils. |
| `22.jpg` | 55 | OK | 100% | 35.2s | $0.0309 | Extraction du vocabulaire et des dialogues avec application stricte des règles de mutation (v-maouez -> vaouez, b-poan -> boan, v-bloaz -> vloaz, p-bleo -> pleo) et suppression des préfixes et parenthèses. Les sections monolingues (Lennadenn, Poelladennou) ont été ignorées. |
| `23.jpg` | 35 | OK | 100% | 34.7s | $0.0249 | Extraction des exemples de conjugaison (p. 42) et du vocabulaire (p. 43) avec application stricte des règles de mutation (ex: ar v-mamm -> ar vamm) et exclusion des mots grammaticaux isolés (e, pe). |
| `27.jpg` | 28 | OK | 100% | 67.5s | $0.0241 | Extraction des dialogues (DIVIZ) et des tableaux de conjugaison. Les formes alternatives de conjugaison (séparées par "ou" ou des espaces) ont été scindées en paires distinctes pour garantir la propreté des segments bretons. |
