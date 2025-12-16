import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzyRiskModel:
    def __init__(self, rule_config):
        """
        rule_config: Словарь с правилом (например, MAX давление 10 МПа)
        """
        self.limit = rule_config['limit_value']
        self.param_name = rule_config['parameter']
        self.type = rule_config['constraint_type']
        
        # Создаем входную переменную (Антецедент)
        # Диапазон: от 0 до 1.5 * лимит (с запасом)
        self.variable = ctrl.Antecedent(np.arange(0, self.limit * 1.5, 0.1), self.param_name)
        
        # Создаем выходную переменную (Консеквент) - Уровень Риска
        self.risk = ctrl.Consequent(np.arange(0, 101, 1), 'risk')
        
        # Определяем функции принадлежности для РИСКА
        self.risk['low'] = fuzz.trimf(self.risk.universe, [0, 0, 50])
        self.risk['medium'] = fuzz.trimf(self.risk.universe, [0, 50, 100])
        self.risk['high'] = fuzz.trimf(self.risk.universe, [50, 100, 100])
        
        # Генерируем функции для ПАРАМЕТРА на основе НТД
        self._generate_membership_functions()
        
    def _generate_membership_functions(self):
        """
        Автоматически создает зоны 'Norm', 'Warning', 'Critical' вокруг лимита НТД.
        """
        if self.type == "MAX":
            # Лимит 10 МПа. 
            # До 80% (8 МПа) - Норма.
            # 80-100% (8-10 МПа) - Предупреждение.
            # > 100% (>10 МПа) - Критично.
            
            limit = self.limit
            self.variable['norm'] = fuzz.trapmf(self.variable.universe, [0, 0, limit*0.8, limit*0.9])
            self.variable['warning'] = fuzz.trimf(self.variable.universe, [limit*0.8, limit*0.95, limit*1.05])
            self.variable['critical'] = fuzz.trapmf(self.variable.universe, [limit*0.95, limit*1.1, limit*1.5, limit*1.5])
            
            # Формируем правила
            self.rules = [
                ctrl.Rule(self.variable['norm'], self.risk['low']),
                ctrl.Rule(self.variable['warning'], self.risk['medium']),
                ctrl.Rule(self.variable['critical'], self.risk['high'])
            ]

    def compute_risk(self, input_value):
        """
        Расчет риска для конкретного значения.
        """
        risk_ctrl = ctrl.ControlSystem(self.rules)
        risk_sim = ctrl.ControlSystemSimulation(risk_ctrl)
        
        risk_sim.input[self.param_name] = input_value
        
        try:
            risk_sim.compute()
            return risk_sim.output['risk']
        except:
            # Если значение за пределами вселенной дискурса
            return 100.0 if input_value > self.limit else 0.0

# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ ---

# Берем правило, которое нашел парсер: "Давление не более 10 МПа"
rule_data = {
    "parameter": "pressure",
    "constraint_type": "MAX",
    "limit_value": 10.0
}

# Инициализируем модель
model = FuzzyRiskModel(rule_data)

# Проверяем разные давления
test_pressures = [5.0, 8.5, 9.8, 10.2, 12.0]

print(f"Анализ риска для ограничения: {rule_data['limit_value']} МПа")
print("-" * 40)
for p in test_pressures:
    risk_score = model.compute_risk(p)
    status = "OK" if risk_score < 30 else "WARNING" if risk_score < 70 else "ALARM"
    print(f"Давление: {p} МПа -> Риск нарушения НТД: {risk_score:.1f}% [{status}]")