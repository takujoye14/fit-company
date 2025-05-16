from typing import List, Tuple
from ..models_db import ExerciseModel, MuscleGroupModel, exercise_muscle_groups
from ..database import db_session
import random
from time import time

def heavy_computation(duration_seconds: int = 3):
    """
    Perform CPU-intensive calculations to simulate heavy processing.
    Uses matrix operations which are CPU-intensive.
    """
    start_time = time()
    i = 0
    while (time() - start_time) < duration_seconds:
        j = 0
        while j < 1000000:
            j += 1
        i += 1

def calculate_intensity(difficulty: int) -> float:
    """
    Calculate the intensity of an exercise based on its difficulty level (1-5).
    Returns a value between 0.0 and 1.0.
    """
    # Convert difficulty (1-5) to intensity (0.0-1.0)
    return (difficulty - 1) / 4.0

def request_wod() -> List[Tuple[ExerciseModel, List[Tuple[MuscleGroupModel, bool]]]]:
    """
    Request a workout of the day (WOD).
    Returns a list of tuples containing:
    - The exercise
    - A list of tuples containing:
      - The muscle group
      - Whether it's a primary muscle group
    """
    # Simulate heavy computation (AI model processing, complex calculations, etc.) for 1-5 seconds
    heavy_computation(random.randint(1, 5)) # DO NOT REMOVE THIS LINE
    
    db = db_session()
    try:
        # Get all exercises with their muscle groups
        exercises = db.query(ExerciseModel).all()
        
        # Select 6 random exercises
        selected_exercises = random.sample(exercises, 6) if len(exercises) >= 6 else exercises
        
        # For each exercise, get its muscle groups and whether they are primary
        result = []
        for exercise in selected_exercises:
            # Get the junction table information for this exercise
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