# benchmark-results-audal
Ce dépôt contient l'ensemble des benchmarks réalisés sur le projet AUDAL. L'ultime version visera à avoir les données complètes, correctes et cohérentes de l'exécution des scripts.

Version : 1.1

## Notes de version :

Nombre de documents texte avec SF = 1 : 200 \
Nombre de tableaux avec SF = 1 : 1000. Le nombre de tableaux est fixe (fixé à 5000) \
Nombre de coeurs utilisés : 5

### Exceptions :

La génération des tableaux a été faite sur 6 coeurs mais est indépendante du reste. \
Pour l'instant, il n'y a que les métriques de PowerJoular. Les métriques d'Humberto seront ajoutées quand les scripts auront tourné au moins une fois...

### Problèmes :

L'exécution du téléchargement des documents ne va pas assez loin dans les PID enfants. \
Les scripts 2 et 3 ne fonctionnent pas correctemment dû au scroll qui est trop court.

### Futurs fixs :

Surveiller de manière récursive tous les PID enfants du PID parent.
Exécuter les requêtes séparément de l'ingestion pour avoir plus de contrôle.
