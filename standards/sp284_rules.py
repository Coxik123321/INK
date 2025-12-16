def sp284_category(probability, consequences):
    if probability < 1e-4 and consequences < 1e6:
        return "Допустимый"
    if probability < 1e-3:
        return "Контролируемый"
    return "Недопустимый"
