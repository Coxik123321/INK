import math

class PipeDefect:
    def __init__(self, length_mm, depth_mm, wall_thickness_mm, diameter_mm, smys_mpa, pressure_mpa):
        """
        Инициализация параметров для расчета по ASME B31G Modified (0.85dL).
        
        :param length_mm: Длина дефекта вдоль оси трубы (L)
        :param depth_mm: Глубина дефекта (d)
        :param wall_thickness_mm: Толщина стенки трубы (t)
        :param diameter_mm: Внешний диаметр трубы (D)
        :param smys_mpa: Предел текучести (Specified Minimum Yield Strength)
        :param pressure_mpa: Рабочее давление в трубе (MAOP)
        """
        self.L = float(length_mm)
        self.d = float(depth_mm)
        self.t = float(wall_thickness_mm)
        self.D = float(diameter_mm)
        self.SMYS = float(smys_mpa)
        self.MAOP = float(pressure_mpa)

    def calculate_b31g_modified(self):
        """
        Расчет безопасного давления (Psafe) и ERF по методике Modified B31G (RSTRENG 0.85 Area).
        """
        # 1. Проверка на сквозной дефект
        if self.d >= self.t:
            return {
                "safe_pressure": 0,
                "erf": 999.9,
                "status": "CRITICAL: LEAK (Утечка)",
                "method": "B31G Modified"
            }

        # 2. Вычисление коэффициента Фолиаса (M) - коэффициент выпучивания
        # z = L^2 / (D * t)
        z = (self.L ** 2) / (self.D * self.t)
        
        if z <= 50:
            M = math.sqrt(1 + 0.6275 * z - 0.003375 * (z**2))
        else:
            M = 0.032 * z + 3.3

        # 3. Напряжение потока (Flow Stress) - для Modified B31G обычно SMYS + 69 MPa (10 ksi)
        # В некоторых версиях 1.1 * SMYS. Используем SMYS + 69 как в стандарте.
        S_flow = self.SMYS + 69.0 

        # 4. Расчет безопасного давления (Psafe)
        # Формула: Psafe = (2 * S_flow * t / D) * ( (1 - 0.85 * d/t) / (1 - 0.85 * d/t / M) )
        
        term1 = (2 * S_flow * self.t) / self.D
        
        d_t_ratio = self.d / self.t
        numerator = 1 - 0.85 * d_t_ratio
        denominator = 1 - 0.85 * d_t_ratio / M
        
        # Защита от деления на ноль в редких случаях
        if denominator == 0:
            denominator = 0.0001
            
        P_safe = term1 * (numerator / denominator)

        # 5. Расчет ERF (Estimated Repair Factor)
        # ERF = MAOP / Psafe. Если ERF > 1, дефект недопустим при текущем давлении.
        ERF = self.MAOP / P_safe if P_safe > 0 else 999.9

        # Определение статуса
        status = "Safe"
        if ERF >= 1.0:
            status = "REPAIR REQUIRED (Ремонт)"
        elif ERF >= 0.9:
            status = "MONITOR (Мониторинг)"

        return {
            "safe_pressure_mpa": round(P_safe, 2),
            "erf": round(ERF, 3),
            "burst_pressure_mpa": round(P_safe, 2), # В контексте B31G Psafe часто приравнивают к Pburst с запасом
            "status": status,
            "folias_factor_M": round(M, 3)
        }

# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ ---
if __name__ == "__main__":
    # Пример: Труба 720 мм, стенка 10 мм, дефект длиной 100 мм и глубиной 4 мм (40% стенки)
    # Сталь К52 (примерно 360 МПа текучесть), давление 5.5 МПа
    defect = PipeDefect(
        length_mm=100, 
        depth_mm=4, 
        wall_thickness_mm=10, 
        diameter_mm=720, 
        smys_mpa=360, 
        pressure_mpa=5.5
    )
    
    result = defect.calculate_b31g_modified()
    
    print("-" * 30)
    print(f"Входные данные: L={defect.L}mm, d={defect.d}mm, P={defect.MAOP}MPa")
    print("-" * 30)
    print(f"Безопасное давление (Psafe): {result['safe_pressure_mpa']} МПа")
    print(f"Коэффициент опасности (ERF): {result['erf']}")
    print(f"Статус: {result['status']}")
    print("-" * 30)