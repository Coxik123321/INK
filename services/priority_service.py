def calculate_priority(risk, remaining_life, estimated_cost):
    life_factor = 1 / max(remaining_life, 0.1)
    cost_factor = min(estimated_cost / 1_000_000, 1)

    priority = (
        0.5 * risk +
        0.3 * life_factor +
        0.2 * cost_factor
    )

    return round(min(priority, 1.0), 3)
