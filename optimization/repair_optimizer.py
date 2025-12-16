import random

def optimize(defects, budget):
    selected = []
    cost = 0

    for d in sorted(defects, key=lambda x: x["risk"], reverse=True):
        if cost + d["repair_cost"] <= budget:
            selected.append(d)
            cost += d["repair_cost"]

    return selected, cost
