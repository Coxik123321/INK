from models.segment import Segment

def optimize_budget(budget):
    segments = Segment.query.filter(
        Segment.estimated_cost != None
    ).all()

    # эффективность = приоритет / стоимость
    ranked = sorted(
        segments,
        key=lambda s: (s.priority or 0) / (s.estimated_cost or 1),
        reverse=True
    )

    selected = []
    spent = 0

    for s in ranked:
        if spent + s.estimated_cost <= budget:
            selected.append(s)
            spent += s.estimated_cost

    return {
        "selected_segments": selected,
        "total_spent": spent,
        "budget_left": budget - spent
    }
