# src/coach/routes/wod_routes.py

from flask import Blueprint, jsonify, request
from services.wod_service import generate_wod

wod_bp = Blueprint("wod", __name__)

@wod_bp.route("/wod", methods=["POST"])
def get_wod():
    data = request.get_json()
    user_email = data.get("user_email")
    exercises = data.get("exercises")

    if not user_email or not exercises:
        return jsonify({"error": "Missing user_email or exercises parameter"}), 400

    wod = generate_wod(user_email, exercises)
    return jsonify(wod), 200
