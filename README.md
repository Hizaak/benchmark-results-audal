# benchmark-results-audal
Ce dépôt contient l'ensemble des benchmarks réalisés sur le projet AUDAL. L'ultime version visera à avoir les données complètes, correctes et cohérentes de l'exécution des scripts.

Version : 1.0

## Notes de version :

Nombre de documents texte avec SF = 1 : 200 \
Nombre de tableaux avec SF = 1 : 1000. Le nombre de tableaux est fixe (fixé à 5000) \
Nombre de coeurs utilisés : 5

### Exceptions :

L'exécution de l'ingestion et des scripts a été faite sur 6 coeurs et non 5 dû à un oubli de ma part... \
La génération des tableaux a été faite sur 6 coeurs mais est indépendante du reste. \
Pour l'instant, il n'y a que les métriques de PowerJoular. Les métriques d'Humberto seront ajoutées quand les scripts auront tourné au moins une fois...

### Problèmes :

Les scripts 2 et 3 ne fonctionnent pas correctemment du au scroll qui est trop court. \
Futur fix : diminuer le nombre de documents || **augmenter le temps de scroll** (privilégié et appliqué)
