def recommend_action(risk, budget):
    if risk == "Critical":
        return "ImmediateShutdown"

    if risk == "High" and budget > 1000000:
        return "Repair"

    if risk == "High" and budget <= 1000000:
        return "PressureReduction"

    return "ContinueOperation"
