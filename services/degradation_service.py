import math
from services.priority_service import calculate_priority
from services.recommendation_service import recommend_action

DEGRADATION_RATE = 0.15  # коэффициент деградации в год

def degrade_segment(segment, years=1):
    segment.risk_level = min(
        float(segment.risk_level) * math.exp(DEGRADATION_RATE * years),
        1.0
    )

    segment.remaining_life = max(segment.remaining_life - years, 0.0)

    segment.priority = calculate_priority(
        risk=float(segment.risk_level),
        remaining_life=segment.remaining_life,
        estimated_cost=segment.estimated_cost or 0
    )

    segment.recommended_action = recommend_action(
        priority=segment.priority,
        risk=float(segment.risk_level),
        remaining_life=segment.remaining_life
    )

    return segment
