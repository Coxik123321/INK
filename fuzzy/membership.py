def low(x, a=0, b=0.3):
    return max(0, min(1, (b - x) / b))

def medium(x, a=0.2, b=0.5, c=0.8):
    if x < a or x > c:
        return 0
    if x < b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)

def high(x, a=0.6, b=1.0):
    return max(0, min(1, (x - a) / (b - a)))
