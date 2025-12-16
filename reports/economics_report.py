# pipeline_ai/reports/economics_report.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_econ_pdf(input_data: dict, econ_result: dict, filename="economics_report.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Отчет: Экономическая оценка воздействия")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    y -= 20

    c.drawString(40, y, "Входные параметры:")
    y -= 15
    for k, v in input_data.items():
        c.drawString(60, y, f"{k}: {v}")
        y -= 12

    y -= 10
    c.drawString(40, y, "Результаты расчета:")
    y -= 15
    for k, v in econ_result.items():
        c.drawString(60, y, f"{k}: {v}")
        y -= 12

    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Рекомендация:")
    y -= 15
    total = econ_result.get("total_impact", 0)
    if total > 5_000_000:
        c.drawString(60, y, "Рекомендуется незамедлительный ремонт. Обосновать финансирование.")
    else:
        c.drawString(60, y, "Ремонт по плану. Рассмотреть оптимизацию затрат.")

    c.showPage()
    c.save()
    return filename
