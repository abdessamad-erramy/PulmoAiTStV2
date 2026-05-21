# 🫁 PulmoAI — Système Intelligent de Détection Pulmonaire

Application Web Flask avec architecture MVC pour la détection automatique des maladies
pulmonaires (Normal / Pneumonie / COVID-19) à partir d'images radiographiques.

---

## 📁 Structure du projet (MVC)

```
PulmoAI/
│
├── app.py                        ← Point d'entrée Flask
├── config.py                     ← Configuration globale
├── requirements.txt              ← Dépendances Python
│
├── 📁 models/                    ── MODÈLE (M)
│   ├── user.py                   ← Gestion des médecins
│   └── analysis.py               ← Gestion des analyses
│
├── 📁 routes/                    ── CONTRÔLEUR (C)
│   ├── auth.py                   ← /login · /logout · /register
│   ├── predict.py                ← /dashboard · /upload · /result/<id>
│   ├── history.py                ← /history
│   └── report.py                 ← /report/<id>
│
├── 📁 services/                  ── SERVICES (logique métier)
│   ├── model_service.py          ← Chargement .h5 + prédiction IA
│   ├── image_service.py          ← Sauvegarde des images uploadées
│   └── pdf_service.py            ← Génération rapport PDF
│
├── 📁 templates/                 ── VUE (V)
│   ├── base.html                 ← Layout commun (sidebar Bootstrap)
│   ├── login.html                ← Connexion + inscription
│   ├── dashboard.html            ← Tableau de bord
│   ├── upload.html               ← Upload + analyse
│   ├── result.html               ← Résultat prédiction
│   └── history.html              ← Historique
│
├── 📁 static/
│   ├── css/style.css             ← Thème sombre personnalisé
│   └── uploads/                  ← Radiographies uploadées
│
├── 📁 database/
│   ├── init_db.py                ← Création tables SQLite
│   └── pulmoai.db                ← Base de données (auto-créée)
│
└── 📁 ai_model/
    └── pulmo_model.h5            ←  VOTRE MODÈLE ICI !
```

---

## ⚙️ Installation et lancement

### Étape 1 — Ouvrir le projet dans VS Code

```bash
cd PulmoAI
code .
```

### Étape 2 — Créer l'environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 — Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 4 — Placer le modèle entraîné

```bash
# Copiez votre fichier dans :
ai_model/pulmo_model.h5
```

### Étape 5 — Lancer l'application

```bash
python app.py
```

### Étape 6 — Ouvrir dans le navigateur

```
http://127.0.0.1:5000
```

---

## 🔁 Flux de l'application

```
Médecin → Login → Dashboard → Upload Radiographie
       → image_service (save) → model_service (InceptionV3)
       → Analysis.save() → SQLite DB
       → result.html (prédiction + probabilités)
       → report.py → pdf_service → Rapport PDF
```

---

##  Important

- Vérifiez l'ordre des classes dans `config.py` :
  ```python
  CLASS_NAMES = ['COVID-19', 'Normal', 'Pneumonie']
  ```
- Ce système est un outil d'aide à la décision uniquement.
- Il ne remplace pas l'avis d'un médecin qualifié.
