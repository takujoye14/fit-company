from flask import Flask, jsonify
from src.stats.models_db import init_db, SessionLocal, WorkoutStat
import os

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "STATS SERVICE UP"}

@app.route("/stats/<string:user_email>", methods=["GET"])
def get_user_stats(user_email):
    try:
        db = SessionLocal()
        stats = db.query(WorkoutStat).filter_by(user_email=user_email).order_by(WorkoutStat.performed_at.desc()).all()
        db.close()

        result = [
            {
                "workout_id": stat.workout_id,
                "user_email": stat.user_email,
                "performed_at": stat.performed_at.isoformat(),
                "exercise_ids": stat.exercise_ids
            }
            for stat in stats
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve stats", "details": str(e)}), 500

def run_app():
    init_db()
    if os.getenv("RUN_CONSUMER") == "1":
        from src.stats.consumer import StatsConsumer
        consumer = StatsConsumer()
        consumer.start()
    else:
        app.run(host="0.0.0.0", port=5002, debug=True)

if __name__ == "__main__":
    run_app()
