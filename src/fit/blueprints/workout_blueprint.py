from flask import Blueprint, g, request, jsonify
from pydantic import ValidationError
from ..models_dto import  RegisterWorkoutSchema
from ..services.workout_service import get_most_recent_workout_exercises, get_user_next_workout, perform_workout, register_workout
from ..services.auth_service import  api_key_required, jwt_required

workout_bp = Blueprint('workout', __name__)
   

@workout_bp.route("/last", methods=["POST"])
@api_key_required
def get_user_last_performed_workout():
    try:
        email = request.json.get("email")
        if not email:
            return jsonify({"error": "email is required"}), 400
        
        exercises = get_most_recent_workout_exercises(email, performed=True)
        if exercises is None:
            return jsonify([]), 200
            
        return jsonify(exercises.exercises), 200
        
    except Exception as e:
        return jsonify({"error": "Error retrieving last workout", "details": str(e)}), 500 
    
@workout_bp.route("/", methods=["POST"])
@api_key_required
def create_workout():
    try:
        workout_data = request.get_json()
        workout = RegisterWorkoutSchema.model_validate(workout_data)
        register_workout(workout.email, workout.exercises)
        return jsonify({"message": "Workout registered successfully"}), 200
        
    except ValidationError as e:
        return jsonify({"error": "Invalid workout data", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Error registering workout", "details": str(e)}), 500 
    
@workout_bp.route("/<int:workout_id>/perform", methods=["POST"])
@jwt_required
def perform_workout_api(workout_id: int):
    try:
        user_email = g.user_email
        perform_workout(workout_id, user_email)
        return jsonify({"message": "Workout marked as performed"}), 200
    except Exception as e:
        return jsonify({"error": "Error marking workout as performed", "details": str(e)}), 500 

@workout_bp.route("/", methods=["GET"])
@jwt_required
def get_next_workout_to_perform():
    try:
        user_email = g.user_email
        exercises = get_user_next_workout(user_email)
        if exercises is None:
            return jsonify({}), 200
        
        return exercises.model_dump_json(), 200
        
    except Exception as e:
        return jsonify({"error": "Error retrieving unperformed workout", "details": str(e)}), 500 
    
@workout_bp.route("/workouts/<int:workout_id>/perform", methods=["POST"])
def perform_workout(workout_id):
    try:
        data = request.get_json()
        user_email = data.get("email")
        exercise_ids = data.get("exercise_ids")

        if not user_email or not exercise_ids:
            return jsonify({"error": "Missing user_email or exercise_ids"}), 400

        db = db_session()
        workout = db.query(WorkoutModel).filter_by(id=workout_id).first()

        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        workout.performed_at = datetime.datetime.utcnow()
        db.commit()

        # Publish the event to RabbitMQ
        event = WorkoutPerformedMessage(
            workout_id=workout_id,
            user_email=user_email,
            performed_at=workout.performed_at,
            exercise_ids=exercise_ids
        )
        rabbitmq_service.publish_workout_performed_event(event)

        return jsonify({"message": "Workout marked as performed"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to mark workout as performed", "details": str(e)}), 500
