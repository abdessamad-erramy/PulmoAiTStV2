import numpy as np
import os
import cv2
from tensorflow.keras.models import load_model

# ══════════════════════════════════════════
#  SERVICE — AI Model
#  Gestion du modèle et des prédictions
# ══════════════════════════════════════════

_model = None
_model_path = None

def _get_model(model_path: str):
    """ Charge le modèle en mode Singleton pour optimiser la mémoire """
    global _model, _model_path
    if _model is None or _model_path != model_path:
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Modèle introuvable : {model_path}\n"
                "→ Vérifiez que le fichier 'pulmo_model.h5' est bien dans ai_model/"
            )
        print(f" Chargement du modèle depuis {model_path}...")
        #  FIXED: load with compile=False to avoid custom optimizer issues (e.g. 'Itao')
        _model = load_model(model_path, compile=False)
        _model_path = model_path
        print(" Modèle chargé avec succès")
    return _model

def predict(img_path, model_path, img_size, class_names):
    """
    Prétraitement de l'image et exécution de l'inférence.
    """
    model = _get_model(model_path)

    #  Use OpenCV exactly like the training code
    image = cv2.imread(img_path)
    if image is None:
        raise ValueError(f"Impossible de lire l'image : {img_path}")
        
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, img_size)           # (224, 224)
    image = np.array(image)                        # NO /255.0 — model trained without it

    image = np.expand_dims(image, axis=0)          # add batch dim → (1, 224, 224, 3)

    preds      = model.predict(image, verbose=0)[0]
    idx        = int(np.argmax(preds))
    label      = class_names[idx]
    confidence = float(round(float(preds[idx]) * 100, 2))

    probabilities = {
        cls: float(round(float(preds[i]) * 100, 2))
        for i, cls in enumerate(class_names)
    }

    return {
        'prediction'   : label,
        'confidence'   : confidence,
        'probabilities': probabilities,
    }
