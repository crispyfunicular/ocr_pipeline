# Instructions spécifiques : Le Gonidec (Vocabulaire 1919)

## Règles d'extraction

- **Extraction des synonymes :** Lorsqu'une vedette française possède plusieurs traductions bretonnes séparées par des virgules, extrayez **chaque traduction bretonne** dans une paire distincte associée au même mot français.
- **Aucun échappement Unicode :** Assurez-vous d'utiliser un formatage pur UTF-8 (pas de symboles comme `\u00e9`). Les accents doivent être lisibles en clair (é, à, è, ô, etc.).

- **Tirets de substitution (`--` ou `—`) :** Le dictionnaire utilise ces tirets cadratins pour remplacer le mot vedette. Lorsque la vedette se présente avec une locution en tête, sous la forme `mot1, mot2 de — : traduction1` (ou avec point-virgule `mot1 ; mot2 de — ...`), il faut **résoudre le tiret** avec le mot vedette. Ainsi, on extraira le `français` sous la forme "mot2 de mot1" (ou selon le sens de la locution) et non pas avec un tiret ou avec la vedette `mot1` seule. Exemple : pour `baryton ; voix de —, krenn-vouez`, il faut écrire `{"français": "voix de baryton", "breton": "krenn-vouez"}`. Si l'entrée simple `mot1` a son propre sens traduit, la sous-entrée contenant le tiret qui la suit reste à ignorer. Le texte français extrait ne doit **jamais** contenir de tiret isolé de la sorte.

- **Verbes pronominaux :** Quand la vedette est un verbe pronominal noté `verbe (s')`, normalisez en plaçant le pronom avant le verbe : `s'accouder` (et non `accouder (s')`).

- **Première lettre tronquée :** La marge gauche peut couper la première lettre de certaines vedettes. Puisque le dictionnaire est classé par ordre alphabétique, il est possible de **deviner la première lettre manquante** à partir de la lettre de section en cours (ex. : si on sait que la page est dans la section « A », une vedette lue `_cheminer` peut être rétablie en `acheminer`). En revanche, si **plusieurs lettres** sont manquantes et que le mot ne peut pas être reconstruit avec certitude, **ignorer l'entrée**.


- **Abréviations :** Les abréviations suivantes (listées sur la page 13) doivent être systématiquement ignorées et ne pas être incluses dans le texte extrait :
  - **act.** = actif.
  - **adj.** = adjectif.
  - **adv.** = adverbe.
  - **col.** = collectif.
  - **conj.** = conjonction.
  - **conjug.** = conjugaison.
  - **Corn.** = Cornouaille.
  - **ex.** = exemple.
  - **f.** = féminin.
  - **fam.** = familier.
  - **fig.** = figuré.
  - **g.** = genre.
  - **infin.** = infinitif.
  - **irrég.** = irrégulier.
  - **Le Gon.** = Le Gonidec.
  - **m.** = masculin.
  - **néol.** = néologisme.
  - **neut.** = neutre.
  - **part.** = participe.
  - **pl.** = pluriel.
  - **prép.** = préposition.
  - **sing.** = singulier.
  - **subst.** = substantif.
  - **suiv.** = suivant.
  - **Trég.** = Tréguier.
  - **U. B.** = unan-bennak, quelqu'un, dans les exemples bretons.
  - **v.** = voyez.
  - **Van.** = Vannes.
  - **verb.** = verbe.
  - **Villem.** = de la Villemarqué.

- **Précisions grammaticales, pluriels et dialectes en breton :** Le dictionnaire indique parfois la préposition à utiliser avec le mot breton (ex: `ouz`), son pluriel (ex: `pl. tud...`, `pl. -zidi`, `pl. -i`, `pl. ...`), son collectif (ex: `col. (penn-ognon)`), son participe (ex: `part. graet`), ou sa variante dialectale (ex: `Van. arouarek`, `Trég. ...`). Ces indications concernent le **mot breton** et ne doivent **absolument pas** se retrouver dans le champ `français` (même si elles sont parfois accompagnées d'une glose comme `à l'égard de`). Le champ `français` ne doit contenir que le mot cible français, expurgé de toutes ces notes de grammaire ou dialecte breton (retirez intégralement les contenus entre parenthèses associés).
  - Exemple : pour l'entrée `inexorable, didruez (ouz, à l'égard de)`, il faut extraire `{"français": "inexorable", "breton": "didruez"}`.
  - Exemple : pour l'entrée `infidèle, dén divadez, pl. tud...`, il faut extraire `{"français": "un infidèle", "breton": "dén divadez"}`.
  - Exemple : pour l'entrée `oignon, ognon, col. (penn-ognon)`, il faut extraire `{"français": "oignon", "breton": "ognon"}`.
  - Exemple : pour l'entrée `oisif, inoccupé accidentellement (Van. arouarek)`, il faut extraire `{"français": "oisif, inoccupé accidentellement", "breton": "dilabour"}` (ou la valeur appropriée selon l'entrée principale).
