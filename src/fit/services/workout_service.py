from datetime import datetime
from typing import List
from ..database import db_session
from ..models_db import  UserExerciseHistory
from ..models_dto import ExerciseId
from sqlalchemy import func

def register_workout(user_email: str, exercise_ids: List[int]):
    """
    Perform a workout for the user
    """
    db = db_session() 
    try:
        # Store the workout in the database
        exercise_date = datetime.now()
        for exercise_id in exercise_ids:
            workout_entry = UserExerciseHistory(
                user_email=user_email,
                exercise_id=exercise_id,
                date=exercise_date
            )
            db.add(workout_entry)
        db.commit()
    finally:
        db.close()

def get_last_workout_exercises(user_email: str):
    """
    Get the exercises from the user's last workout
    """
    db = db_session()
    try:
        # Get the most recent workout date for this user
        last_workout_date = db.query(func.max(UserExerciseHistory.date)).filter(
            UserExerciseHistory.user_email == user_email
        ).scalar()
        
        if not last_workout_date:
            return None
            
        # Get exercises from the last workout
        last_workout = db.query(
            UserExerciseHistory
        ).filter(
            UserExerciseHistory.user_email == user_email,
            UserExerciseHistory.date == last_workout_date
        ).all()
        
        result = []
        for exercise in last_workout:
            
            exercise_dto = ExerciseId.model_validate(
                {
                    "id": exercise.exercise_id,
                }
            )
            
            result.append(exercise_dto)
            
        return result
    finally:
        db.close() 