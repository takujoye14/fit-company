from datetime import datetime
from typing import List, Optional
from ..database import db_session
from ..models_db import UserExerciseHistory, WorkoutModel
from ..models_dto import ExerciseId
from sqlalchemy import func

def register_workout(user_email: str, exercise_ids: List[int]):
    """
    Create a new workout for the user with the specified exercises.
    The workout is created with created_at set to now, but performed_at as null.
    """
    db = db_session() 
    try:
        # Create a new workout
        workout = WorkoutModel(
            user_email=user_email,
            created_at=datetime.utcnow(),
            performed_at=None
        )
        db.add(workout)
        db.flush()  # Flush to get the workout ID
        
        # Add exercises to the workout
        for exercise_id in exercise_ids:
            exercise_entry = UserExerciseHistory(
                workout_id=workout.id,
                exercise_id=exercise_id
            )
            db.add(exercise_entry)
        
        db.commit()
    finally:
        db.close()

def get_most_recent_workout_exercises(user_email: str, performed: bool) -> Optional[List[ExerciseId]]:
    """
    Get the exercises from the user's most recent workout based on its performed status.
    
    Args:
        user_email (str): The email of the user
        performed (bool): If True, returns the last performed workout. If False, returns the last unperformed workout.
    
    Returns:
        Optional[List[ExerciseId]]: List of exercise IDs or None if no matching workout exists.
    """
    db = db_session()
    try:
        # Build the query based on performed status
        query = db.query(WorkoutModel).filter(
            WorkoutModel.user_email == user_email
        )
        
        if performed:
            query = query.filter(WorkoutModel.performed_at.isnot(None))
            query = query.order_by(WorkoutModel.performed_at.desc())
        else:
            query = query.filter(WorkoutModel.performed_at.is_(None))
            query = query.order_by(WorkoutModel.created_at.desc())
            
        last_workout = query.first()
        
        if not last_workout:
            return None
            
        # Get exercises from the last workout
        exercises = db.query(
            UserExerciseHistory
        ).filter(
            UserExerciseHistory.workout_id == last_workout.id
        ).all()
        
        result = []
        for exercise in exercises:
            exercise_dto = ExerciseId.model_validate(
                {
                    "id": exercise.exercise_id,
                }
            )
            result.append(exercise_dto)
            
        return result
    finally:
        db.close()

def perform_workout(workout_id: int, user_email: str):
    """
    Mark a workout as performed by setting its performed_at timestamp.
    """
    db = db_session()
    try:
        workout = db.query(WorkoutModel).filter(
            WorkoutModel.id == workout_id
        ).first()
        
        if workout and workout.user_email == user_email:
            workout.performed_at = datetime.utcnow()
            db.commit()
        else:
            raise Exception("Workout not found or user does not have access to this workout")
    finally:
        db.close()