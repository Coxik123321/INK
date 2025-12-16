import json

def export_point(lon, lat, properties, filename):
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat]
        },
        "properties": properties
    }

    geojson = {
        "type": "FeatureCollection",
        "features": [feature]
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
