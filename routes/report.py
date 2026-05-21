from flask import Blueprint, make_response, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from models.analysis import Analysis
from services.pdf_service import generate_pdf

report_bp = Blueprint('report', __name__)

# ══════════════════════════════════════════
#  CONTROLLER — Report  (C in MVC)
# ══════════════════════════════════════════

@report_bp.route('/report/<int:analysis_id>')
@login_required
def download_report(analysis_id):
    db       = current_app.config['DATABASE']
    analysis = Analysis.get_by_id(analysis_id, db)

    if not analysis:
        flash('Analyse introuvable.', 'danger')
        return redirect(url_for('predict.dashboard_page'))

    # Attach probabilities dict for PDF
    # analysis['probabilities'] = {
    #     'COVID-19' : analysis.get('prob_covid',  0),
    #     'Normal'   : analysis.get('prob_normal', 0),
    #     'Pneumonie': analysis.get('prob_pneum',  0),
    # }
    analysis['probabilities'] = {
    'Covid'    : analysis.get('prob_covid',  0),
    'Normal'   : analysis.get('prob_normal', 0),
    'Pneumonia': analysis.get('prob_pneum',  0),
}

    pdf_bytes = generate_pdf(analysis, current_user)

    response = make_response(pdf_bytes)
    response.headers['Content-Type']        = 'application/pdf'
    response.headers['Content-Disposition'] = \
        f'attachment; filename=PulmoAI_Rapport_{analysis_id}.pdf'
    return response
