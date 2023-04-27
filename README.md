# benchmark-results-audal
Ce dépôt contient l'ensemble des benchmarks réalisés sur le projet AUDAL. L'ultime version visera à avoir les données complètes, correctes et cohérentes de l'exécution des scripts.

Version : 1.2

## Notes de version :

Nombre de documents texte avec SF = 1 : 200 \
Nombre de tableaux avec SF = 1 : 1000. Le nombre de tableaux est fixe (fixé à SF 5 = 5000) \
Scales utilisées : 1 3 5 (200 600 1000) \
Nombre de coeurs utilisés : 5

## TODO :

- Powerjoular :
    1. Tableaux : ...
    2. Documents : OK
    3. Ingestion : OK
    4. Requêtes : ...

- Métriques maison :
    1. Tableaux : ...
    2. Documents : ...
    3. Ingestion : ...
    4. Requêtes : ...


### Exceptions :

Pour l'instant, il n'y a que les métriques de PowerJoular (mais elles sont presque complètes pour l'urgence de vendredi).
Les métriques d'Humberto seront ajoutées quand les scripts auront tourné au moins une fois...

### Problèmes :

L'exécution du téléchargement des documents ne va pas assez loin dans les PID enfants. \
Les scripts 2 et 3 ne fonctionnent pas correctemment dû au scroll qui est trop court.

### Futurs fixs :

Exécuter les requêtes séparément de l'ingestion pour avoir plus de contrôle.
