from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.segment import Segment
from decision_engine.decision_pipeline import make_decision
from database import db
from models.pipeline import Pipeline
from models.pipeline_segment import PipelineSegment
from decision_engine.segment_decision import evaluate_segment
from database import db
decision_api = Blueprint("decision_api", __name__)

@decision_api.route("/decision/run", methods=["POST"])
@jwt_required()
def run_decision():
    segments = Segment.query.all()

    for s in segments:
        result = make_decision(s)
        s.decision_risk = result["risk"]
        s.recommended_action = result["action"]
        s.estimated_cost = result["cost"]

    db.session.commit()
    return jsonify({"status": "decisions updated"})



@decision_api.route("/decision/run_segments", methods=["POST"])
def run_segment_decisions():
    segments = PipelineSegment.query.all()

    for s in segments:
        pipeline = Pipeline.query.get(s.pipeline_id)
        risk, action = evaluate_segment(s, pipeline)

        s.risk = risk
        s.recommended_action = action

    db.session.commit()
    return {"status": "segment decisions updated"}