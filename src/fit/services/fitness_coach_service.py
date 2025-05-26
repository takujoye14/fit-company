from typing import List, Tuple
from datetime import date
from ..models_db import ExerciseModel, MuscleGroupModel, exercise_muscle_groups, ExerciseHistoryModel
from ..database import db_session
import random
from time import time

def heavy_computation(duration_seconds: int = 3):
    start_time = time()
    i = 0
    while (time() - start_time) < duration_seconds:
        j = 0
        while j < 1000000:
            j += 1
        i += 1

def calculate_intensity(difficulty: int) -> float:
    return (difficulty - 1) / 4.0

def request_wod(user_email: str) -> List[Tuple[ExerciseModel, List[Tuple[MuscleGroupModel, bool]]]]:
    heavy_computation(random.randint(1, 5))  # DO NOT REMOVE THIS LINE

    db = db_session()
    try:
        # Get exercise IDs from yesterday for this user
        yesterday = date.today().toordinal() - 1
        yesterday_exercises = db.query(ExerciseHistoryModel.exercise_id).filter(
            ExerciseHistoryModel.user_email == user_email,
            ExerciseHistoryModel.performed_at == date.fromordinal(yesterday)
        ).all()
        excluded_ids = [e.exercise_id for e in yesterday_exercises]

        # Get exercises excluding yesterday's
        all_exercises = db.query(ExerciseModel).filter(~ExerciseModel.id.in_(excluded_ids)).all()

        # Pick 6
        selected_exercises = random.sample(all_exercises, 6) if len(all_exercises) >= 6 else all_exercises

        # Log today's history
        today = date.today()
        for ex in selected_exercises:
            db.add(ExerciseHistoryModel(user_email=user_email, exercise_id=ex.id, performed_at=today))
        db.commit()

        # Return with muscle groups
        result = []
        for exercise in selected_exercises:
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