import random

def simulate(years, failure_prob):
    accidents = 0
    for _ in range(years):
        if random.random() < failure_prob:
            accidents += 1
    return accidents
