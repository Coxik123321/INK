# pipeline_ai/simulation/whatif.py
from copy import deepcopy

def what_if_scenario(defect, changes: dict):
    """
    defect: dict with keys risk, remaining_life, cathodic_protection (0..1), pressure (0..1)
    changes: dict, e.g. {"pressure_delta": 0.1, "cp_effectiveness": -0.2, "budget_cut": 0.5}
    Возвращает модельный итог: new_risk, recommended_action, est_cost_change
    """
    d = deepcopy(defect)
    # apply pressure change
    if "pressure_delta" in changes:
        d["pressure"] = max(0, min(1.5, d.get("pressure", 0.7) + changes["pressure_delta"]))

    # change cathodic protection effectiveness (0..1)
    if "cp_effectiveness" in changes:
        d["cathodic_protection"] = max(0, min(1, d.get("cathodic_protection", 0.8) + changes["cp_effectiveness"]))

    # naive risk model: risk increases with pressure, decreases with cp
    base_risk = d.get("risk", 0.5)
    risk = base_risk * (1 + 0.6 * (d["pressure"] - 0.7)) * (1 - 0.5 * (d["cathodic_protection"] - 0.5))
    risk = max(0.0, min(1.0, risk))

    # cost change roughly proportional to risk change
    est_cost_change = (risk - base_risk) * 2_000_000

    recommended_action = "Monitor"
    if risk > 0.8:
        recommended_action = "ImmediateRepair"
    elif risk > 0.5:
        recommended_action = "ScheduleRepair"

    return {
        "original_risk": base_risk,
        "new_risk": round(risk, 3),
        "est_cost_delta": int(est_cost_change),
        "recommended_action": recommended_action,
        "scenario_applied": changes
    }
