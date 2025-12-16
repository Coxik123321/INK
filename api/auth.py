from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from app import db

auth_api = Blueprint("auth_api", __name__)

@auth_api.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
    )

    return jsonify(access_token=token)
