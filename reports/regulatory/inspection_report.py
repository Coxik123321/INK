from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_inspection_report(filename, fields: dict):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("ОТЧЕТ О ТЕХНИЧЕСКОМ СОСТОЯНИИ ТРУБОПРОВОДА", styles["Title"]))

    for k, v in fields.items():
        content.append(Paragraph(f"<b>{k}</b>: {v}", styles["Normal"]))

    doc.build(content)
