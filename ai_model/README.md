# 📁 ai_model/

## Placez votre modèle ici

```
ai_model/
└── pulmo_model.h5    ← VOTRE modèle InceptionV3 entraîné
```

## Comment exporter votre modèle depuis votre script d'entraînement

```python
# À la fin de votre script d'entraînement :
model.save('ai_model/pulmo_model.h5')
print("Modèle sauvegardé !")
```

## Ordre des classes (IMPORTANT)

Vérifiez que l'ordre dans config.py correspond à votre entraînement :

```python
CLASS_NAMES = ['COVID-19', 'Normal', 'Pneumonie']
#               index 0     index 1   index 2
```

Si votre ordre est différent, modifiez `CLASS_NAMES` dans `config.py`.

## Paramètres attendus

- Taille d'entrée : 299 × 299 pixels (InceptionV3)
- Normalisation   : pixels / 255.0
- Sorties         : 3 probabilités (softmax)
