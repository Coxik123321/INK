from flask import Blueprint, jsonify, request
from app import db
from models.segment import Segment
from services.geojson_service import build_geojson
from services.priority_service import calculate_priority
from services.recommendation_service import recommend_action
from flask_jwt_extended import jwt_required
from services.auth_service import role_required

segments_api = Blueprint("segments_api", __name__)


@segments_api.route("/segments", methods=["GET"])
@jwt_required()
@role_required("analyst", "engineer", "admin")
def get_segments():
    return jsonify(build_geojson())

@segments_api.route("/segments", methods=["POST"])
@jwt_required()
@role_required("engineer", "admin")
def create_segment():
    data = request.json

    priority = calculate_priority(
        risk=data["risk"],
        remaining_life=data["remaining_life"],
        estimated_cost=data.get("estimated_cost", 0)
    )

    action = recommend_action(
        priority=priority,
        risk=data["risk"],
        remaining_life=data["remaining_life"]
    )

    segment = Segment(
        lat=data["lat"],
        lon=data["lon"],
        priority=priority,
        risk_level=data.get("risk_level"),
        remaining_life=data["remaining_life"],
        estimated_cost=data.get("estimated_cost"),
        recommended_action=action
    )

    db.session.add(segment)
    db.session.commit()

    return jsonify({
        "status": "ok",
        "id": segment.id,
        "priority": priority,
        "action": action
    })
