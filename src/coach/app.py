import datetime
from flask import Flask, request, jsonify
import os
import logging
from .fitness_data_init import init_fitness_data
from .fitness_service import get_exercises_by_muscle_group, get_all_exercises, get_exercise_by_id
from .database import init_db, db_session
from .models_db import GeneratedWODModel

# Configure Flask logging
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Force stdout to be unbuffered
import sys
sys.stdout.reconfigure(line_buffering=True)

# Validate required environment variables
if not os.getenv("FIT_API_KEY"):
    raise RuntimeError("FIT_API_KEY environment variable must be set")

@app.route("/health")
def health():
    return {"status": "UP"}

@app.route("/exercises", methods=["GET"])
def get_exercises():
    try:
        muscle_group_id = request.args.get("muscle_group_id")
        if muscle_group_id:
            exercises = get_exercises_by_muscle_group(int(muscle_group_id))
        else:
            exercises = get_all_exercises()
        return jsonify([ex.model_dump() for ex in exercises]), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving exercises", "details": str(e)}), 500

@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    try:
        exercise = get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404
        return jsonify(exercise.model_dump()), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving exercise", "details": str(e)}), 500

@app.route("/wod/<email>", methods=["GET"])
def get_user_wod(email):
    session = db_session()
    try:
        wod = session.query(GeneratedWODModel).filter_by(user_email=email).all()
        wod_exercises = []
        for ex in wod:
            wod_exercises.append({
                "exercise_name": ex.exercise_name,
                "suggested_weight": ex.suggested_weight,
                "suggested_reps": ex.suggested_reps,
                "created_at": ex.created_at.isoformat()
            })
        response = {
            "wod": wod_exercises,
            "generated_at": datetime.datetime.utcnow().isoformat()
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

def run_app():
    init_db()
    init_fitness_data()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    run_app()
