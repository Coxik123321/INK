from decision_engine.action_selector import select_action

def evaluate_segment(segment, pipeline):
    age = 2025 - pipeline.commissioning_year
    pressure_factor = segment.operating_pressure / pipeline.max_pressure

    risk = (
        0.45 * segment.corrosion_rate +
        0.35 * min(age / 50, 1) +
        0.20 * min(pressure_factor, 1)
    )

    risk = round(min(risk, 1.0), 3)
    action = select_action(risk)

    return risk, action
