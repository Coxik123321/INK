import numpy as np
import skfuzzy as fuzz

depth = np.arange(0, 101, 1)

depth_sets = {
    "Low": fuzz.trimf(depth, [0, 0, 20]),
    "Medium": fuzz.trimf(depth, [20, 40, 60]),
    "High": fuzz.trimf(depth, [40, 60, 80]),
    "Extreme": fuzz.trimf(depth, [60, 100, 100])
}

def fuzzify_depth(value):
    return {
        k: fuzz.interp_membership(depth, v, value)
        for k, v in depth_sets.items()
    }
