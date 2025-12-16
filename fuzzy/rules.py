from fuzzy.membership import low, medium, high

def evaluate_priority(risk, remaining_life):
    rules = []

    # ПРАВИЛО 1
    r1 = min(high(risk), low(remaining_life))
    rules.append(("Высокий приоритет", r1,
                  "СП 366.1325800.2017, п. 7.3"))

    # ПРАВИЛО 2
    r2 = min(medium(risk), medium(remaining_life))
    rules.append(("Средний приоритет", r2,
                  "ОСТ 153-39.4-010-2002, п. 6.2"))

    # ПРАВИЛО 3
    r3 = min(low(risk), high(remaining_life))
    rules.append(("Низкий приоритет", r3,
                  "РД 03-606-03"))

    return rules
