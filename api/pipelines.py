from flask import Blueprint, jsonify
from models.pipeline_segment import PipelineSegment
from geoalchemy2.shape import to_shape

pipelines_api = Blueprint("pipelines_api", __name__)

@pipelines_api.route("/pipelines/geojson", methods=["GET"])
def pipelines_geojson():
    features = []

    segments = PipelineSegment.query.all()

    for s in segments:
        geom = to_shape(s.geometry)

        features.append({
            "type": "Feature",
            "geometry": geom.__geo_interface__,
            "properties": {
                "segment_id": s.id,
                "risk": s.risk,
                "action": s.recommended_action
            }
        })

    return jsonify({
        "type": "FeatureCollection",
        "features": features
    })
