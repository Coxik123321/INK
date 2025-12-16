from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from models.segment import Segment

def generate_report(filepath):
    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(
        "<b>Pipeline Risk Assessment Report</b>",
        styles["Title"]
    ))

    segments = Segment.query.order_by(
        Segment.priority.desc()
    ).all()

    for s in segments:
        content.append(Paragraph(
            f"Segment {s.id}: "
            f"Priority={s.priority}, "
            f"Action={s.recommended_action}, "
            f"Cost={s.estimated_cost}",
            styles["Normal"]
        ))

    doc.build(content)
