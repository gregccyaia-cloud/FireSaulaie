# Passerelle Gerland - La Saulaie | Étude incendie V1.4 complète

## Installation et exécution

```bash
python -m pip install -r requirements.txt
python main.py
```

Le rapport et les graphiques sont écrits dans `results/`.
Les options `SHOW_PLOTS` et `GENERATE_REPORT` sont dans `config.py`.

## Arborescence

- `main.py` : orchestration et sélection du cas critique à 30 min ;
- `config.py` : paramètres ;
- `fire.py` : courbes ISO 834 et feu extérieur ;
- `geometry.py` : géométrie simplifiée et distances 3D ;
- `thermal.py` : bilan thermique ;
- `plotting.py` : graphiques Matplotlib ;
- `report.py` : rapport Word, équations OMML et annexe détaillée ;
- `assets/` : huit images projet ;
- `results/` : graphiques et rapport générés.

## Limite importante

La V1.4 utilise Φ = 1,0. Les longueurs de foyer 10/15/20 m sont paramétrées, mais n'influent pas encore sur le flux tant qu'un facteur de forme géométrique n'est pas introduit.
