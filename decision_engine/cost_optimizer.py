def estimate_cost(segment, action):
    if action == "Immediate repair":
        return segment.length_km * 120_000
    if action == "Scheduled repair":
        return segment.length_km * 60_000
    if action == "Inspection":
        return segment.length_km * 15_000
    return 0
