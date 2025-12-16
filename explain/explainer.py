def explain_decision(defect, pressure, risk):
    explanation = []

    if defect["depth_percent"] > 40:
        explanation.append("Большая глубина дефекта")

    if pressure > 0.8:
        explanation.append("Высокое рабочее давление")

    explanation.append(f"Итоговый риск: {risk}")

    return explanation
