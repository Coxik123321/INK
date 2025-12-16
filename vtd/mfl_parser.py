def parse_mfl(signal, calibration_factor):
    """
    Преобразование MFL-сигнала в глубину дефекта
    """
    depth_percent = signal * calibration_factor
    return min(depth_percent, 100)
