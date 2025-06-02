# src/coach/services/wod_service.py

import time
import random

def heavy_computation(duration_seconds: int = 3):
    start_time = time.time()
    while (time.time() - start_time) < duration_seconds:
        i = 0
        while i < 1000000:
            i += 1

def generate_wod(user_email: str):
    heavy_computation(random.randint(1, 5))
    # Dummy WOD data
    wod = []
    for i in range(6):
        wod.append({
            "id": i + 1,
            "name": f"Exercise {i+1}",
            "description": f"Description for exercise {i+1}",
            "difficulty": random.randint(1, 5),
            "suggested_weight": round(random.uniform(5.0, 50.0), 2),
            "suggested_reps": random.randint(8, 15)
        })
    return wod
