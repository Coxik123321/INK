from sklearn.linear_model import LinearRegression
import numpy as np



def forecast_defect(segment):
    # Сортируем дефекты по времени
    records = sorted(segment.records, key=lambda r: r.date)
    
    if len(records) < 2:
        return None  # Мало данных для прогноза

    # Преобразуем время в количество дней с первого дефекта
    times = np.array([(r.date - records[0].date).days for r in records]).reshape(-1, 1)
    values = np.array([r.priority for r in records]).reshape(-1, 1)

    # Линейная регрессия
    model = LinearRegression()
    model.fit(times, values)

    # Прогноз на следующие 30 дней (например)
    future_time = np.array([[times[-1][0] + 30]])  # 30 дней от последнего дефекта
    predicted_value = model.predict(future_time)

    return predicted_value[0][0]  # Предсказанное значение приоритетности


def calculate_priority(defect_type, base_priority, pressure=None):
    type_weight = {
        "corrosion": 1.2,
        "crack": 1.5,
        "dent": 1.0,
        "weld": 1.3
    }

    pressure_factor = 1.0
    if pressure:
        if pressure > 7.5:
            pressure_factor = 1.3
        elif pressure > 5.0:
            pressure_factor = 1.15

    priority = base_priority * type_weight.get(defect_type, 1.0) * pressure_factor
    return round(min(priority, 1.0), 2)


def recommend_action(priority):
    if priority >= 0.8:
        return "Immediate repair"
    elif priority >= 0.6:
        return "Scheduled repair"
    elif priority >= 0.4:
        return "Inspection"
    else:
        return "Monitoring"
