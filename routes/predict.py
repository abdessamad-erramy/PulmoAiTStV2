from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import login_required, current_user
from services.image_service import save_upload, fetch_image_from_url
from services.model_service import predict, _get_model
from services.gradcam_service import generate_gradcam
from services.image_preprocessing import (
    preprocess_image_xray,
    preprocess_image_for_visualization,
    save_gradcam_with_alpha
)
from models.analysis import Analysis

import os
import numpy as np

predict_bp = Blueprint('predict', __name__)

# ══════════════════════════════════════════
#  VIEWS — Render Pages
# ══════════════════════════════════════════

@predict_bp.route('/dashboard')
@login_required
def dashboard_page():
    db     = current_app.config['DATABASE']
    total  = Analysis.count_by_user(current_user.id, db)
    recent = Analysis.get_by_user(current_user.id, db, limit=5)
    return render_template('dashboard.html', total=total, recent=recent, user=current_user)


@predict_bp.route('/upload')
@login_required
def upload_page():
    return render_template('upload.html', user=current_user)


@predict_bp.route('/result/<int:analysis_id>')
@login_required
def result_page(analysis_id):
    db       = current_app.config['DATABASE']
    analysis = Analysis.get_by_id(analysis_id, db)

    if not analysis or str(analysis['user_id']) != str(current_user.id):
        return redirect(url_for('predict.dashboard_page'))

    try:
        rel = os.path.relpath(
            analysis['image_path'], start=current_app.root_path
        ).replace('\\', '/')
        analysis['image_url'] = '/' + rel

        base, ext    = os.path.splitext(analysis['image_path'])
        heatmap_path = f"{base}_gradcam{ext}"
        rel_h        = os.path.relpath(
            heatmap_path, start=current_app.root_path
        ).replace('\\', '/')
        analysis['heatmap_url'] = '/' + rel_h
    except Exception:
        pass

    return render_template('result.html', a=analysis, user=current_user)


# ══════════════════════════════════════════
#  API ENDPOINTS — Controller
# ══════════════════════════════════════════

@predict_bp.route('/api/dashboard', methods=['GET'])
@jwt_required()
def dashboard_api():
    user_id = get_jwt_identity()
    db      = current_app.config['DATABASE']
    total   = Analysis.count_by_user(user_id, db)
    recent  = Analysis.get_by_user(user_id, db, limit=5)

    return jsonify({
        "user_id"         : user_id,
        "total_analyses"  : total,
        "recent_analyses" : recent
    }), 200


@predict_bp.route('/api/predict', methods=['POST'])
@predict_bp.route('/upload', methods=['POST'])
def run_prediction():
    """
    Main prediction endpoint:
    1. Identify user (JWT or session)
    2. Load and save uploaded image
    3. Run AI prediction
    4. Generate Grad-CAM heatmap
    5. Save analysis to database
    6. Return results with visualization URLs
    """

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 0. IDENTIFY USER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    user_id = None

    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        from flask_jwt_extended import decode_token
        auth_header = request.headers.get('Authorization')
        if auth_header and 'Bearer ' in auth_header:
            try:
                token   = auth_header.split(' ')[1]
                user_id = decode_token(token)['sub']
            except Exception:
                pass

    if not user_id:
        return jsonify({'error': 'Non autorisé'}), 401

    cfg      = current_app.config
    img_path = None

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 1. GET IMAGE (upload or URL)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            try:
                img_path = save_upload(
                    file,
                    cfg['UPLOAD_FOLDER'],
                    cfg['ALLOWED_EXTENSIONS']
                )
            except Exception as e:
                return jsonify({'error': str(e)}), 400

    elif request.is_json:
        data      = request.get_json()
        image_url = data.get('image_url')
        if image_url:
            try:
                img_path = fetch_image_from_url(
                    image_url,
                    cfg['UPLOAD_FOLDER'],
                    cfg['ALLOWED_EXTENSIONS']
                )
            except Exception as e:
                return jsonify({'error': str(e)}), 400

    if not img_path:
        return jsonify({'error': 'Aucune image ou URL fournie.'}), 400

    try:
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2. RUN AI PREDICTION
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        result = predict(
            img_path    = img_path,
            model_path  = cfg['MODEL_PATH'],
            img_size    = cfg['IMG_SIZE'],
            class_names = cfg['CLASS_NAMES'],
        )
        probs = result['probabilities']

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 3. PREPARE IMAGES FOR GRAD-CAM
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        model = _get_model(cfg['MODEL_PATH'])

        # Float [0,1] with batch dim → model input
        img_array = preprocess_image_xray(
            img_path,
            target_size=cfg['IMG_SIZE']
        )

        # uint8 (0-255), shape (H, W, 3) → visualization only
        original_array = preprocess_image_for_visualization(
            img_path,
            target_size=cfg['IMG_SIZE']
        )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 4. GENERATE GRAD-CAM HEATMAP
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        gradcam_result = generate_gradcam(
            model                = model,
            img_array            = img_array,       # float [0,1]
            last_conv_layer_name = cfg.get('LAST_CONV_LAYER', 'mixed10'),
            image_original       = original_array,  # uint8 (0-255) ✅
        )

        heatmap = gradcam_result['heatmap']

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 5. SAVE HEATMAP TO DISK
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        base, ext    = os.path.splitext(img_path)
        heatmap_path = f"{base}_gradcam{ext}"

        # original_array is uint8 (0-255) — no conversion needed ✅
        save_gradcam_with_alpha(
            heatmap,
            original_array,   # uint8 (0-255)
            heatmap_path,
            alpha=0.4
        )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 6. SAVE ANALYSIS TO DATABASE
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        analysis_id = Analysis.save(
            user_id     = user_id,
            image_path  = img_path,
            prediction  = result['prediction'],
            confidence  = result['confidence'],
            prob_covid  = probs.get('Covid',     0),
            prob_normal = probs.get('Normal',    0),
            prob_pneum  = probs.get('Pneumonia', 0),
            db_path     = cfg['DATABASE'],
        )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 7. BUILD RESPONSE URLs
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        rel_path    = os.path.relpath(img_path,     start=current_app.root_path).replace('\\', '/')
        rel_heatmap = os.path.relpath(heatmap_path, start=current_app.root_path).replace('\\', '/')

        return jsonify({
            'success'        : True,
            'analysis_id'    : analysis_id,
            'prediction'     : result['prediction'],
            'confidence'     : result['confidence'],
            'probabilities'  : probs,
            'image_url'      : '/' + rel_path,
            'heatmap_url'    : '/' + rel_heatmap,
            'predicted_class': gradcam_result['predicted_class']
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erreur lors de l\'analyse : {str(e)}'}), 500