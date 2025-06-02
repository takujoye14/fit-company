# src/coach/routes/wod_routes.py

from flask import Blueprint, jsonify, request
from src.coach.services.wod_service import generate_wod

wod_bp = Blueprint("wod", __name__)

@wod_bp.route("/wod", methods=["GET"])
def get_wod():
    user_email = request.args.get("user_email")
    if not user_email:
        return jsonify({"error": "Missing user_email parameter"}), 400

    wod = generate_wod(user_email)
    return jsonify(wod), 200
