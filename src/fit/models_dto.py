from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Union
from datetime import datetime

# User-related DTOs
class UserSchema(BaseModel):
    email: EmailStr
    name: str
    role: str
class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserResponseSchema(UserSchema):
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str
 
class UserProfileSchema(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_goal: Optional[str] = None
    onboarded: Optional[str] = "false"

class UserProfileResponseSchema(BaseModel):
    email: str
    name: str

class UserProfileUpdate(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_goal: Optional[str] = None
    onboarded: Optional[str] = None

class User(UserSchema):
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_goal: Optional[str] = None
    onboarded: str = "false"

# Muscle Group DTOs
class MuscleGroupBase(BaseModel):
    name: str
    body_part: str
    description: Optional[str] = None

class MuscleGroupUpdate(BaseModel):
    name: Optional[str] = None
    body_part: Optional[str] = None
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

class ExerciseCreate(ExerciseBase):
    muscle_groups: List[ExerciseMuscleGroup]

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    equipment: Optional[str] = None
    instructions: Optional[str] = None
    muscle_groups: Optional[List[ExerciseMuscleGroup]] = None

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
