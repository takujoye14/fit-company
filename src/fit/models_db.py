from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

class UserModel(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Profile information (nullable as they'll be filled during onboarding)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    fitness_goal = Column(String, nullable=True)
    onboarded = Column(String, default="false", nullable=False)

    def __repr__(self):
        return f"<User(email='{self.email}', name='{self.name}', role='{self.role}')>" 