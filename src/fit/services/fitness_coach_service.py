from typing import List, Tuple
from datetime import date
import requests
from ..models_db import ExerciseModel, MuscleGroupModel, exercise_muscle_groups, ExerciseHistoryModel
from ..database import db_session

COACH_SERVICE_URL = "http://coach:5002/wod"

def calculate_intensity(difficulty: int) -> float:
    return (difficulty - 1) / 4.0

def request_wod(user_email: str) -> List[Tuple[ExerciseModel, List[Tuple[MuscleGroupModel, bool]]]]:
    db = db_session()
    try:
        # Step 1: Fetch yesterday's exercise IDs
        yesterday = date.today().toordinal() - 1
        yesterday_exercises = db.query(ExerciseHistoryModel.exercise_id).filter(
            ExerciseHistoryModel.user_email == user_email,
            ExerciseHistoryModel.performed_at == date.fromordinal(yesterday)
        ).all()
        excluded_ids = [e.exercise_id for e in yesterday_exercises]

        # Step 2: Fetch all exercises from the DB and filter out yesterday's
        all_exercises = db.query(ExerciseModel).all()
        filtered_exercises = [
            {
                "id": ex.id,
                "name": ex.name,
                "description": ex.description,
                "difficulty": ex.difficulty
            }
            for ex in all_exercises if ex.id not in excluded_ids
        ]
    finally:
        db.close()

    # Step 3: Send filtered exercises to coach microservice
    try:
        response = requests.post(
            COACH_SERVICE_URL,
            json={"user_email": user_email, "exercises": filtered_exercises}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch WOD from coach service: {e}")

    wod_exercises = response.json()

    # Step 4: Log today's history in the local DB
    db = db_session()
    try:
        today = date.today()
        selected_exercises = []

        for ex in wod_exercises:
            db.add(ExerciseHistoryModel(user_email=user_email, exercise_id=ex["id"], performed_at=today))
            selected_exercises.append(ex["id"])

        db.commit()

        # Fetch exercise details from the local DB
        exercises = db.query(ExerciseModel).filter(ExerciseModel.id.in_(selected_exercises)).all()

        # For each exercise, get muscle groups
        result = []
        for exercise in exercises:
            stmt = db.query(
                MuscleGroupModel,
                exercise_muscle_groups.c.is_primary
            ).join(
                exercise_muscle_groups,
                MuscleGroupModel.id == exercise_muscle_groups.c.muscle_group_id
            ).filter(
                exercise_muscle_groups.c.exercise_id == exercise.id
            )
            muscle_groups = [(mg, is_primary) for mg, is_primary in stmt.all()]
            result.append((exercise, muscle_groups))

        return result
    finally:
        db.close()