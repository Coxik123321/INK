from flask import Blueprint, jsonify

health_api = Blueprint("health_api", __name__)

@health_api.route("/api/health")
def health():
    return jsonify({"status": "ok"})
