import json

# Тестовые сегменты/точки трубопровода
segments = [
    {"id": 1, "type": "point", "coordinates": [55.751244, 37.618423], "priority": 0.2, "estimated_cost": 1_200_000, "action": "Monitor"},
    {"id": 2, "type": "point", "coordinates": [56.838926, 60.605702], "priority": 0.8, "estimated_cost": 3_500_000, "action": "ImmediateRepair"},
    {"id": 3, "type": "point", "coordinates": [59.934280, 30.335099], "priority": 0.5, "estimated_cost": 2_100_000, "action": "ScheduleRepair"},
    {"id": 4, "type": "point", "coordinates": [54.983333, 73.366667], "priority": 0.4, "estimated_cost": 900_000, "action": "Monitor"},
    {"id": 5, "type": "point", "coordinates": [55.030199, 82.920430], "priority": 0.7, "estimated_cost": 2_900_000, "action": "ScheduleRepair"},
    {"id": 6, "type": "point", "coordinates": [53.195873, 50.100193], "priority": 0.9, "estimated_cost": 4_200_000, "action": "ImmediateRepair"}
]

geojson = {
    "type": "FeatureCollection",
    "features": []
}

for s in segments:
    geojson["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Point" if s["type"] == "point" else "LineString",
            "coordinates": s["coordinates"]
        },
        "properties": {
            "segment_id": s["id"],
            "priority": s["priority"],
            "estimated_cost": s["estimated_cost"],
            "action": s["action"]
        }
    })

# Сохраняем файл в корень проекта (чтобы map.html его видел)
filename = "pipeline_risk.geojson"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print(f"Файл {filename} успешно создан с {len(segments)} сегментами!")
