from flask import Flask, request, jsonify
import jwt
import os

from .billing_service import mark_user_premium, is_user_premium, notify_monolith
from .database import get_user_by_email

SECRET_KEY = os.getenv("JWT_SECRET", "fit-secret-key")

app = Flask(__name__)

@app.route("/api/billing/subscribe", methods=["POST"])
def subscribe():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = decoded.get("sub")  # Match how auth service encodes it

        if not email:
            return jsonify({"error": "Invalid token: missing email"}), 400

        user = get_user_by_email(email)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Mark in DB using email
        mark_user_premium(email)

        # Notify monolith
        notify_monolith(email)

        return jsonify({
            "message": "Payment simulated. User upgraded to premium.",
            "email": email,
            "fake_checkout_id": "dummy_checkout_12345"
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


@app.route("/api/billing/status", methods=["GET"])
def check_premium():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = decoded.get("sub")  # Match how auth service encodes it

        if not email:
            return jsonify({"error": "Invalid token: missing email"}), 400

        user = get_user_by_email(email)
        if not user:
            return jsonify({"error": "User not found"}), 404

        premium = is_user_premium(email)

        return jsonify({"email": email, "is_premium": premium}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


if __name__ == "__main__":
    app.run(debug=True)
