from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from models.segment import Segment
from services.degradation_service import degrade_segment

simulation_api = Blueprint("simulation_api", __name__)

@simulation_api.route("/simulate", methods=["POST"])
@jwt_required()
def simulate_degradation():
    years = request.json.get("years", 1)

    segments = Segment.query.all()

    for s in segments:
        degrade_segment(s, years)

    db.session.commit()

    return jsonify({
        "status": "ok",
        "years_simulated": years,
        "segments_updated": len(segments)
    })
