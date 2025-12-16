def repair_cost(priority_score):
    if priority_score > 0.5:
        return 5_000_000
    if priority_score > 0.2:
        return 2_000_000
    return 500_000
