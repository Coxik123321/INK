import json

def export_geojson(segments, filename="pipeline_risk.geojson"):
    features = []
    for s in segments:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point" if s.get("type","segment")=="point" else "LineString",
                "coordinates": s["coordinates"]
            },
            "properties": {
                "segment_id": s.get("id"),
                "priority": s.get("priority", 0),
                "estimated_cost": s.get("estimated_cost", 0),
                "action": s.get("action", "None")
            }
        })
    geojson = {"type": "FeatureCollection", "features": features}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    return filename
