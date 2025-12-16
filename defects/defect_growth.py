def defect_priority(risk: float, remaining_life: float) -> float:
    """
    Расчет приоритета ремонта дефекта
    """
    if remaining_life <= 0:
        raise ValueError("remaining_life must be > 0")

    return risk * (1 / remaining_life)
