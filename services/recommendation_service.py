def recommend_action(priority, risk, remaining_life):
    if priority >= 0.85 or remaining_life < 0.5:
        return "Immediate repair"
    elif priority >= 0.65 or risk >= 0.7:
        return "Scheduled repair"
    elif priority >= 0.4:
        return "Inspection"
    else:
        return "Monitoring"
