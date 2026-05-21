from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for, flash
from flask_jwt_extended import create_access_token
from flask_login import login_user, logout_user, login_required
from models.user import User

auth_bp = Blueprint('auth', __name__)

# ══════════════════════════════════════════
#  VIEWS — Render Pages
# ══════════════════════════════════════════

@auth_bp.route('/')
@auth_bp.route('/login')
def login_page():
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))

# ══════════════════════════════════════════
#  CONTROLLER — Auth Actions (Form & API)
# ══════════════════════════════════════════

@auth_bp.route('/api/login', methods=['POST', 'GET'])
def login():
    # Handle both POST and redirect if accessed via GET
    if request.method == 'GET':
        return redirect(url_for('auth.login_page'))

    # Detect if request is JSON or Form
    is_json  = request.is_json
    data     = request.get_json() if is_json else request.form
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    db       = current_app.config['DATABASE']

    user_data, hashed_pw = User.get_by_username(username, db)

    if user_data and User.verify_password(password, hashed_pw):
        # 1. Start Web Session (for Flask-Login)
        login_user(user_data)
        
        # 2. Generate JWT (for API)
        access_token = create_access_token(identity=str(user_data.id))
        
        if is_json:
            return jsonify(access_token=access_token), 200
        else:
            return redirect(url_for('predict.dashboard_page'))

    if is_json:
        return jsonify({"msg": "Identifiants incorrects"}), 401
    else:
        flash("Identifiants incorrects", "danger")
        return redirect(url_for('auth.login_page'))


@auth_bp.route('/api/register', methods=['POST'])
def register():
    is_json = request.is_json
    data    = request.get_json() if is_json else request.form
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    nom      = data.get('nom', '').strip()
    prenom   = data.get('prenom', '').strip()
    db       = current_app.config['DATABASE']

    if not username or not password:
        if is_json: return jsonify({"msg": "Champs requis"}), 400
        flash("Nom d'utilisateur et mot de passe requis", "warning")
        return redirect(url_for('auth.login_page'))

    if User.create(username, password, nom, prenom, db):
        if is_json: return jsonify({"msg": "Compte créé"}), 201
        flash("Compte créé avec succès. Connectez-vous.", "success")
        return redirect(url_for('auth.login_page'))
    else:
        if is_json: return jsonify({"msg": "Utilisateur déjà pris"}), 409
        flash("Ce nom d'utilisateur est déjà pris", "danger")
        return redirect(url_for('auth.login_page'))
