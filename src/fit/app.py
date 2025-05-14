from flask import Flask, request, jsonify
from pydantic import ValidationError
from .models_dto import UserSchema
from .services.user_service import create_user as create_user_service
from .services.user_service import get_all_users as get_all_users_service
from .database import init_db

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "UP"}

@app.route("/users", methods=["POST"])
def create_user():
    try:
        user_data = request.get_json()
        user = UserSchema.model_validate(user_data)
        created_user = create_user_service(user)
        return jsonify(created_user.model_dump()), 201
    except ValidationError as e:
        return jsonify({"error": "Invalid user data", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Error creating user", "details": str(e)}), 500

@app.route("/users", methods=["GET"])
def get_all_users():
    try:
        users = get_all_users_service()
        return jsonify([user.model_dump() for user in users]), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving users", "details": str(e)}), 500

def run_app():
    """Entry point for the application script"""
    # Initialize the database before starting the app
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    run_app()

