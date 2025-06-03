from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, Table, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .database import Base
import datetime

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


class UserExerciseHistory(Base):
    __tablename__ = 'user_exercise_history'
    
    id = Column(Integer, primary_key=True)
    user_email = Column(String, ForeignKey('users.email'), nullable=False) 
    exercise_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False, default=datetime.date.today)
    user = relationship("UserModel")

    def __repr__(self):
        return f"<UserExerciseHistory(id={self.id}, user_email='{self.user_email}', exercise_id='{self.exercise_id}', date='{self.date}')>"