from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.segment import Segment
from sqlalchemy import func

analytics_api = Blueprint("analytics_api", __name__)

@analytics_api.route("/analytics/summary", methods=["GET"])
@jwt_required()
def summary():
    total = Segment.query.count()

    high = Segment.query.filter(Segment.priority >= 0.8).count()
    medium = Segment.query.filter(
        Segment.priority >= 0.4,
        Segment.priority < 0.8
    ).count()
    low = Segment.query.filter(Segment.priority < 0.4).count()

    avg_priority = db.session.query(
        func.avg(Segment.priority)
    ).scalar()

    urgent = Segment.query.filter(
        Segment.recommended_action == "Immediate repair"
    ).count()

    return jsonify({
        "total_segments": total,
        "risk_distribution": {
            "high": high,
            "medium": medium,
            "low": low
        },
        "average_priority": round(avg_priority or 0, 3),
        "urgent_repairs": urgent
    })
