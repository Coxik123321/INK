from models.segment import Segment

def build_geojson():
    features = [s.to_feature() for s in Segment.query.all()]
    return {
        "type": "FeatureCollection",
        "features": features
    }
