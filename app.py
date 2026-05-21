from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from config import Config
from database.init_db import init_db
from models.user import User

app = Flask(__name__)
app.config.from_object(Config)

# ── Init database on startup
init_db(app.config['DATABASE'])

# ── Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id), app.config['DATABASE'])

# ── Flask-JWT-Extended setup
jwt = JWTManager(app)

# ── Register Blueprints (Controllers)
from routes.auth    import auth_bp
from routes.predict import predict_bp
from routes.history import history_bp
from routes.report  import report_bp

app.register_blueprint(auth_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(history_bp)
app.register_blueprint(report_bp)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
