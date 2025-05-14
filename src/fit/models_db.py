from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

class UserModel(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(email='{self.email}', name='{self.name}', role='{self.role}')>" 