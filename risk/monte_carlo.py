import random

def monte_carlo_failure(pf, pop, runs=10000):
    failures = 0
    for _ in range(runs):
        strength = random.gauss(pf, pf * 0.1)
        if strength < pop:
            failures += 1
    return failures / runs
