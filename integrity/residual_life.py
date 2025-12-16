def residual_life(depth_now, corrosion_rate, critical_depth):
    """
    мм, мм/год, мм
    """
    return max(
        (critical_depth - depth_now) / corrosion_rate,
        0
    )
