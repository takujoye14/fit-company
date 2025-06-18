from flask import Flask, request, jsonify
import jwt
import os

# Your secret or public key, used to decode token
SECRET_KEY = os.getenv("JWT_SECRET", "secret")

user_premium_status = {}

app = Flask(__name__)

@app.route("/api/billing/subscribe", methods=["POST"])
def subscribe():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = decoded.get("email")  # or "sub" if you're using sub for ID
        if not email:
            return jsonify({"error": "Invalid token: missing email"}), 400

        # Simulate billing
        user_premium_status[email] = True

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
        email = decoded.get("email")
        if not email:
            return jsonify({"error": "Invalid token: missing email"}), 400

        is_premium = user_premium_status.get(email, False)
        return jsonify({"email": email, "is_premium": is_premium})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(debug=True)