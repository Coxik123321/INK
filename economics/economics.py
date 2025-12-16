from math import exp



def total_cost(repair_cost, downtime_cost, risk_penalty):
    return repair_cost + downtime_cost + risk_penalty

def risk_penalty(risk):
    penalties = {
        "Low": 0,
        "Medium": 100000,
        "High": 500000,
        "Critical": 2000000
    }
    return penalties.get(risk, 0)
# pipeline_ai/economics/economics.py


def repair_cost_estimate(base_cost, complexity_factor=1.0, urgency_factor=1.0):
    """
    Простейшая модель стоимости ремонта:
    base_cost — базовая стоимость по ФЕР/ГЭСН (руб)
    complexity_factor — множитель за сложность (1..3)
    urgency_factor — множитель за срочность (1..2)
    """
    return base_cost * complexity_factor * urgency_factor

def opex_impact(downtime_days, daily_loss):
    return downtime_days * daily_loss

def capex_impact(repair_cost):
    return repair_cost

def risk_penalty_numeric(risk_level):
    # risk_level 0..1
    return int(2_000_000 * risk_level)  # шаблонно

def total_economic_impact(base_cost, complexity_factor, urgency_factor, downtime_days, daily_loss, risk_level):
    repair = repair_cost_estimate(base_cost, complexity_factor, urgency_factor)
    opex = opex_impact(downtime_days, daily_loss)
    penalty = risk_penalty_numeric(risk_level)
    total = repair + opex + penalty
    return {
        "repair_cost": repair,
        "opex_loss": opex,
        "risk_penalty": penalty,
        "total_impact": total
    }

def utility_score(risk_reduction, budget, weight_risk=0.7, weight_budget=0.3):
    """
    Простая функция полезности: чем больше снижение риска и чем в рамках бюджета — тем выше.
    """
    return weight_risk * risk_reduction + weight_budget * (1.0 if budget >= 0 else 0)
