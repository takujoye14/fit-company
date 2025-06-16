from sqlalchemy import Column, Integer, String, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import datetime

Base = declarative_base()

class WorkoutStat(Base):
    __tablename__ = "workout_stats"

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, nullable=False)
    user_email = Column(String, nullable=False)
    performed_at = Column(DateTime, default=datetime.datetime.utcnow)
    exercise_ids = Column(JSON, nullable=False)

# Database setup
DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
