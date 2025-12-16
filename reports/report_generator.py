from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_report(filename, data):
    c = canvas.Canvas(filename, pagesize=A4)
    text = c.beginText(40, 800)

    text.textLine("Отчет по оценке технического состояния трубопровода")
    text.textLine("")
    for k, v in data.items():
        text.textLine(f"{k}: {v}")

    c.drawText(text)
    c.showPage()
    c.save()
