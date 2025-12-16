def parse_ut(thickness_nominal, thickness_measured):
    loss = thickness_nominal - thickness_measured
    return (loss / thickness_nominal) * 100
