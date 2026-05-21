import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)

BLUE   = colors.HexColor('#1e3a8a')
GREEN  = colors.HexColor('#16a34a')
RED    = colors.HexColor('#dc2626')
YELLOW = colors.HexColor('#ca8a04')
LGREY  = colors.HexColor('#f1f5f9')
DGREY  = colors.HexColor('#475569')


def generate_pdf(analysis: dict, user) -> bytes:
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=2.5*cm
    )

    styles = getSampleStyleSheet()
    story = []

    usable_width = A4[0] - 4*cm  # 17 cm usable

    # ─────────────────────────────────────────────
    # HEADER CONTENT (Dynamic content drawn later)
    # ─────────────────────────────────────────────

    doc_name = f"Dr. {user.prenom} {user.nom}".strip() or user.username
    date_str = analysis.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M'))
    ana_id   = analysis.get('id', '—')
    pred     = analysis.get('prediction', '—')
    conf     = analysis.get('confidence', 0)

    color = RED if pred.lower() in ['pneumonie', 'pneumonia'] \
        else (YELLOW if 'covid' in pred.lower() else GREEN)

    # ─────────────────────────────────────────────
    # RESULT SECTION
    # ─────────────────────────────────────────────

    story.append(Paragraph("Résultat de l'Analyse IA", styles['Heading2']))
    story.append(HRFlowable(width="100%", thickness=0.7, color=colors.HexColor('#e2e8f0')))
    story.append(Spacer(1, 0.4*cm))

    result_style = ParagraphStyle(
        'ResultStyle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=color,
        fontName='Helvetica-Bold',
        spaceAfter=6
    )

    story.append(Paragraph(f"Diagnostic : {pred.upper()}", result_style))
    story.append(Paragraph(f"Score de confiance : <b>{conf:.1f}%</b>", styles['Normal']))
    story.append(Spacer(1, 0.7*cm))

    # ─────────────────────────────────────────────
    # PROBABILITIES TABLE
    # ─────────────────────────────────────────────

    probs = analysis.get('probabilities', {})

    story.append(Paragraph("Probabilités par Classe", styles['Heading3']))
    story.append(Spacer(1, 0.3*cm))

    prob_data = [['Classe', 'Probabilité (%)', 'Interprétation']]

    for cls, pct in sorted(probs.items(), key=lambda x: x[1], reverse=True):
        interp = "Résultat principal" if cls == pred else "—"
        prob_data.append([cls, f"{pct:.1f}%", interp])

    prob_table = Table(
        prob_data,
        colWidths=[5*cm, 4*cm, usable_width - 9*cm]
    )

    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LGREY]),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#cbd5e1')),
        ('ALIGN', (1,1), (1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    story.append(prob_table)
    story.append(Spacer(1, 0.8*cm))

    # ─────────────────────────────────────────────
    # DISCLAIMER
    # ─────────────────────────────────────────────

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#92400e'),
        backColor=colors.HexColor('#fef9c3'),
        borderPadding=6,
        leading=12
    )

    story.append(Paragraph(
        "⚠️ AVERTISSEMENT IMPORTANT : Ce rapport est généré automatiquement "
        "par un système d'intelligence artificielle à titre d'aide à la décision uniquement. "
        "Il ne remplace en aucun cas l'avis d'un médecin qualifié.",
        disclaimer_style
    ))

    # ─────────────────────────────────────────────
    # HEADER & FOOTER FUNCTIONS
    # ─────────────────────────────────────────────

    def draw_header_footer(canvas, doc):
        canvas.saveState()

        # HEADER
        canvas.setFont("Helvetica-Bold", 16)
        canvas.setFillColor(BLUE)
        canvas.drawCentredString(A4[0]/2, A4[1]-2*cm,
                                 "PulmoAI — Rapport de Diagnostic Pulmonaire")

        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(DGREY)
        canvas.drawCentredString(
            A4[0]/2, A4[1]-2.5*cm,
            "Système Intelligent d'Aide à la Détection des Maladies Pulmonaires par Rayon X"
        )

        canvas.line(2*cm, A4[1]-2.8*cm, A4[0]-2*cm, A4[1]-2.8*cm)

        # FOOTER
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(DGREY)

        canvas.drawString(2*cm, 1.5*cm,
                          f"ID Analyse : #{ana_id} | Médecin : {doc_name}")

        canvas.drawRightString(
            A4[0]-2*cm, 1.5*cm,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    doc.build(story, onFirstPage=draw_header_footer,
              onLaterPages=draw_header_footer)

    return buffer.getvalue()