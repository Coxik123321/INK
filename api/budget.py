from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.budget_optimization_service import optimize_budget

budget_api = Blueprint("budget_api", __name__)

@budget_api.route("/budget/optimize", methods=["POST"])
@jwt_required()
def optimize():
    budget = request.json.get("budget")

    if not budget:
        return jsonify({"error": "Budget not specified"}), 400

    result = optimize_budget(budget)

    return jsonify({
        "budget": budget,
        "total_spent": result["total_spent"],
        "budget_left": result["budget_left"],
        "segments": [
            {
                "id": s.id,
                "priority": s.priority,
                "cost": s.estimated_cost,
                "action": s.recommended_action
            } for s in result["selected_segments"]
        ]
    })
