def select_action(risk):
    if risk >= 0.8:
        return "Immediate repair"
    if risk >= 0.5:
        return "Scheduled repair"
    if risk >= 0.3:
        return "Inspection"
    return "Monitoring"
