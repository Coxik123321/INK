def evaluate_risk(segment):
    """
    Возвращает интегральный риск 0..1
    """
    corrosion = segment.corrosion_rate
    age = segment.age_years
    pressure = segment.operating_pressure

    risk = (
        0.5 * corrosion +
        0.3 * min(age / 50, 1) +
        0.2 * min(pressure / segment.max_pressure, 1)
    )

    return round(min(risk, 1.0), 3)
