class PipelineTwin:
    def __init__(self, pressure, temperature, defects):
        self.pressure = pressure
        self.temperature = temperature
        self.defects = defects

    def apply_scenario(self, delta_pressure=0):
        self.pressure += delta_pressure
        return self.evaluate()

    def evaluate(self):
        risk = 0
        for d in self.defects:
            risk += d["depth_percent"] * self.pressure
        return risk
