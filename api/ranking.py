def defect_priority(risk, remaining_life):
    score = 0
    if risk == "Critical":
        score += 100
    elif risk == "High":
        score += 70
    elif risk == "Medium":
        score += 40

    if remaining_life < 1:
        score += 50
    elif remaining_life < 3:
        score += 30

    return score
