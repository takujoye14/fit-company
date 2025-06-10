from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime, date

# Muscle Group DTOs
class MuscleGroupBase(BaseModel):
    name: str
    body_part: str
    description: Optional[str] = None

class MuscleGroup(MuscleGroupBase):
    id: int

# Exercise DTOs
class ExerciseMuscleGroup(BaseModel):
    muscle_group_id: int
    is_primary: bool = False

class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    difficulty: int = Field(..., ge=1, le=5)
    equipment: Optional[str] = None
    instructions: Optional[str] = None

class MuscleGroupWithPrimary(MuscleGroup):
    is_primary: bool

class Exercise(ExerciseBase):
    id: int
    muscle_groups: List[MuscleGroupWithPrimary] = []

class MuscleGroupImpact(BaseModel):
    id: int
    name: str
    body_part: str
    is_primary: bool
    intensity: float  # Calculated based on exercise difficulty (0.0 to 1.0)

class WodExerciseSchema(BaseModel):
    id: int
    name: str
    description: str
    difficulty: int
    muscle_groups: List[MuscleGroupImpact]
    suggested_weight: float = 0.0  # Default weight suggestion
    suggested_reps: int = 10  # Default number of reps

class WodResponseSchema(BaseModel):
    exercises: List[WodExerciseSchema]
    generated_at: datetime

class CreateWodMessage(BaseModel):
    user_email: str
    date: date
    attempt: int = Field(default=0, ge=0, le=3)