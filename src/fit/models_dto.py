from pydantic import BaseModel
from typing import Optional

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
