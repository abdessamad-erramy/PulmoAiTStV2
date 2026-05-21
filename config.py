import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Flask Configuration"""
    SECRET_KEY         = 'pulmoai-secret-key-2024'
    JWT_SECRET_KEY     = 'jwt-secret-key-9988'  # For Flask-JWT-Extended
    UPLOAD_FOLDER      = os.path.join(BASE_DIR, 'static', 'uploads')
    MODEL_PATH         = os.path.join(BASE_DIR, 'ai_model', 'pulmo_model.h5')
    DATABASE           = os.path.join(BASE_DIR, 'database', 'pulmoai.db')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # IMAGE & MODEL SETTINGS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    IMG_SIZE    = (224, 224)  # InceptionV3 input size
    CLASS_NAMES = ['Covid', 'Normal', 'Pneumonia']  # Must match training order

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # GRAD-CAM SETTINGS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    LAST_CONV_LAYER = 'mixed10'  # Last convolutional layer in InceptionV3
    # Note: CLASSIFIER_LAYERS removed - we use the full model's output directly