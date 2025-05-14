from ..models_dto import UserSchema, UserResponseSchema
from ..models_db import UserModel
from ..database import db_session
from typing import List
import random
import string
import hashlib

def generate_random_password(length=10):
    """Generate a random password of specified length"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(user: UserSchema) -> UserResponseSchema:
    """
    Create a new user with a random password and persist it to the database
    """
    # Generate a random password
    random_password = generate_random_password()
    hashed_password = hash_password(random_password)
    
    # Convert Pydantic model to SQLAlchemy model
    db_user = UserModel(
        email=user.email,
        name=user.name,
        role=user.role,
        password_hash=hashed_password
    )
    
    # Add and commit to database
    db = db_session()
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    
    # Return response including the clear-text password (one-time reveal)
    response = UserResponseSchema(
        email=user.email,
        name=user.name,
        role=user.role,
        password=random_password
    )
    
    return response

def get_all_users() -> List[UserSchema]:
    """
    Retrieve all users from the database
    """
    db = db_session()
    try:
        # Query all users from the database
        db_users = db.query(UserModel).all()
        
        # Convert SQLAlchemy models to Pydantic models
        return [
            UserSchema(
                email=db_user.email,
                name=db_user.name,
                role=db_user.role
            )
            for db_user in db_users
        ]
    finally:
        db.close()
