import math

def b31g_failure_pressure(D, t, L, d, SMYS):
    A = 0.893 * math.sqrt(L / (D * t))
    M = math.sqrt(1 + A**2)
    Pf = (2 * SMYS * t / D) * (1 - d / t) / M
    return Pf

def safety_factor(P_allowable, P_operating):
    return P_allowable / P_operating
