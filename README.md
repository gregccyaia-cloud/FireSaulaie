# Étude incendie - version E autonome

```bash
python -m pip install -r requirements.txt
python main.py
```

Le rapport est généré sous `results/reports/`. Toutes les images sont embarquées sous `assets/`.

## Vérification structurelle préliminaire

Les données E et NQP sont intégrées. Le rapport calcule la contrainte nominale, le module réduit et la déformation élastique indicative. Un ratio de résistance conforme et un temps maximal justifié nécessitent encore, pour chaque organe, la section métallique résistante réelle et la résistance caractéristique à 20 °C. Ces champs sont explicitement signalés comme non renseignés, sans valeur inventée.
