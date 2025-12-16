def predict_defect_growth(
    depth,
    corrosion_rate,
    years,
    wall_thickness
):
    new_depth = depth + corrosion_rate * years

    risk = min(new_depth / wall_thickness, 1.0)

    remaining_life = max(
        (wall_thickness - new_depth) / corrosion_rate,
        0.0
    )

    return {
        "depth": round(new_depth, 4),
        "risk": round(risk, 3),
        "remaining_life": round(remaining_life, 2)
    }
