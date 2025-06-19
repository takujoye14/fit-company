from pydantic import BaseModel

class CreateWodMessage(BaseModel):
    email: str
    is_premium: bool
