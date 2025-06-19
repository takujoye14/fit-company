from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreateWodMessage(BaseModel):
    email: str
    is_premium: bool
    
class WorkoutPerformedMessage(BaseModel):
    workout_id: int
    user_email: str
    performed_at: datetime
    exercise_ids: List[int]