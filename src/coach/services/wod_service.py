import time
import random

def heavy_computation(duration_seconds: int = 3):
    start_time = time.time()
    while (time.time() - start_time) < duration_seconds:
        i = 0
        while i < 1000000:
            i += 1

def generate_wod(user_email: str, exercises: list[dict]) -> list[dict]:
    """
    Generate a WOD by picking 6 exercises from the provided list.
    """
    heavy_computation(random.randint(1, 5))

    # Select up to 6 exercises (less if there aren't enough)
    wod = random.sample(exercises, min(len(exercises), 6))

    # Add suggested_weight and suggested_reps to each exercise
    for ex in wod:
        ex["suggested_weight"] = round(random.uniform(5.0, 50.0), 2)
        ex["suggested_reps"] = random.randint(8, 15)

    return wod
