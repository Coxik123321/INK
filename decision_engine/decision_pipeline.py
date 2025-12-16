from decision_engine.risk_evaluator import evaluate_risk
from decision_engine.action_selector import select_action
from decision_engine.cost_optimizer import estimate_cost

def make_decision(segment):
    risk = evaluate_risk(segment)
    action = select_action(risk)
    cost = estimate_cost(segment, action)

    explanation = {
        "risk_factors": {
            "corrosion": segment.corrosion_rate,
            "age": segment.age_years,
            "pressure": segment.operating_pressure
        },
        "computed_risk": risk,
        "selected_action": action,
        "estimated_cost": cost
    }

    return {
        "risk": risk,
        "action": action,
        "cost": cost,
        "explanation": explanation
    }
