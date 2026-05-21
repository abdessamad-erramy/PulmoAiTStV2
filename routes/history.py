from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from models.analysis import Analysis

history_bp = Blueprint('history', __name__)

# ══════════════════════════════════════════
#  CONTROLLER — History  (C in MVC)
# ══════════════════════════════════════════

@history_bp.route('/history')
@login_required
def history():
    db       = current_app.config['DATABASE']
    analyses = Analysis.get_by_user(current_user.id, db)
    return render_template('history.html', analyses=analyses, user=current_user)
