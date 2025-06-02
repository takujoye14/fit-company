# src/coach/services/wod_service.py

import time
import random

def heavy_computation(duration_seconds: int = 3):
    start_time = time.time()
    while (time.time() - start_time) < duration_seconds:
        i = 0
        while i < 1000000:
            i += 1

def generate_wod(user_email: str, excluded_ids: list[int] = None):
    """
    Generate a WOD excluding exercises with IDs in excluded_ids.
    """
    heavy_computation(random.randint(1, 5))

    all_possible_exercises = [
        {
            "id": i + 1,
            "name": f"Exercise {i+1}",
            "description": f"Description for exercise {i+1}",
            "difficulty": random.randint(1, 5),
            "suggested_weight": round(random.uniform(5.0, 50.0), 2),
            "suggested_reps": random.randint(8, 15)
        }
        for i in range(20)  # Let's assume we have 20 exercises to choose from
    ]

    if excluded_ids:
        filtered_exercises = [
            ex for ex in all_possible_exercises if ex["id"] not in excluded_ids
        ]
    else:
        filtered_exercises = all_possible_exercises

    # Select up to 6 exercises (less if there aren't enough)
    wod = random.sample(filtered_exercises, min(len(filtered_exercises), 6))

    return wod
