from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from models.segment import Segment
from services.defect_growth_service import predict_defect_growth
from services.priority_service import calculate_priority
from services.recommendation_service import recommend_action

defects_api = Blueprint("defects_api", __name__)

@defects_api.route("/defects/predict", methods=["POST"])
@jwt_required()
def predict_defects():
    data = request.json
    years = data.get("years", 1)

    segment = Segment.query.get(data["segment_id"])
    if not segment:
        return jsonify({"error": "Segment not found"}), 404

    result = predict_defect_growth(
        depth=segment.depth,
        corrosion_rate=segment.corrosion_rate,
        years=years,
        wall_thickness=segment.wall_thickness
    )

    segment.depth = result["depth"]
    segment.remaining_life = result["remaining_life"]

    segment.priority = calculate_priority(
        risk=result["risk"],
        remaining_life=segment.remaining_life,
        estimated_cost=segment.estimated_cost or 0
    )

    segment.recommended_action = recommend_action(
        priority=segment.priority,
        risk=result["risk"],
        remaining_life=segment.remaining_life
    )

    db.session.commit()

    return jsonify({
        "segment_id": segment.id,
        "years": years,
        "risk": result["risk"],
        "remaining_life": result["remaining_life"],
        "priority": segment.priority,
        "action": segment.recommended_action
    })
