def defuzzify(rules):
    weights = {
        "Низкий приоритет": 0.2,
        "Средний приоритет": 0.5,
        "Высокий приоритет": 0.9
    }

    numerator = 0
    denominator = 0

    for label, strength, _ in rules:
        numerator += weights[label] * strength
        denominator += strength

    if denominator == 0:
        return 0

    return numerator / denominator
