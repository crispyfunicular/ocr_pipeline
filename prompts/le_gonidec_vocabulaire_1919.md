# Instructions spécifiques : Le Gonidec (Vocabulaire 1919)

## Règles d'extraction

- **Une seule paire par vedette :** Pour chaque vedette française (en italique ou en caractères espacés), n'extrayez qu'**une seule paire** : la vedette comme `français` et sa **toute première traduction bretonne** comme `breton`. Ignorez toutes les traductions suivantes, les synonymes, les sous-entrées, les sous-mots en italique et les exemples.

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
