from pydantic import BaseModel, Field
from typing import Optional, Literal

class UserSchema(BaseModel):
    email: str
    name: str
    role: str

class UserResponseSchema(UserSchema):
    password: Optional[str] = None

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class LoginSchema(BaseModel):
    email: str
    password: str

class UserProfileSchema(BaseModel):
    weight: float = Field(gt=0, description="Weight in kilograms")
    height: float = Field(gt=0, description="Height in centimeters")
    fitness_goal: Literal["weight_loss", "muscle_gain", "endurance"] = Field(
        description="Fitness goal: weight_loss, muscle_gain, or endurance"
    )

class UserProfileResponseSchema(BaseModel):
    email: str
    name: str
    weight: Optional[float] = None
    height: Optional[float] = None
    fitness_goal: Optional[str] = None
    onboarded: str
