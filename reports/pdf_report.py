from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(data, result, rules, filename="defect_report.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Отчет по анализу дефекта трубопровода")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 20

    c.drawString(40, y, "Входные данные:")
    y -= 15
    c.drawString(60, y, f"Интегральный риск: {data['risk']}")
    y -= 15
    c.drawString(60, y, f"Остаточный ресурс: {data['remaining_life']} лет")
    y -= 30

    c.drawString(40, y, f"Рассчитанный приоритет ремонта: {round(result, 3)}")
    y -= 30

    c.drawString(40, y, "Сработавшие правила:")
    y -= 20

    for r in rules:
        c.drawString(60, y, f"- {r['rule']} (μ={r['strength']})")
        y -= 15
        c.drawString(80, y, f"НТД: {r['normative']}")
        y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Вывод:")
    y -= 15
    c.setFont("Helvetica", 10)

    if result > 0.7:
        c.drawString(60, y, "Рекомендуется первоочередной ремонт.")
    elif result > 0.4:
        c.drawString(60, y, "Рекомендуется плановый ремонт.")
    else:
        c.drawString(60, y, "Допускается эксплуатация с контролем.")

    c.showPage()
    c.save()

    return filename
