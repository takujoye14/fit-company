# src/coach/routes/wod_routes.py

from flask import Blueprint, jsonify, request
from services.wod_service import generate_wod

wod_bp = Blueprint("wod", __name__)

@wod_bp.route("/wod", methods=["POST"])
def get_wod():
    data = request.get_json()

    user_email = data.get("user_email")
    excluded_ids = data.get("excluded_ids", [])

    if not user_email:
        return jsonify({"error": "Missing user_email parameter"}), 400

    wod = generate_wod(user_email, excluded_ids)
    return jsonify(wod), 200
