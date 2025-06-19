import os
from sqlalchemy import Column, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"

    email = Column(String, primary_key=True)
    is_premium = Column(Boolean, nullable=False, default=False)

# Use env var or fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:docker@billing-db:5432/billing")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
