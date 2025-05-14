from ..models_dto import UserSchema
from ..models_db import UserModel
from ..database import db_session
from typing import List

def create_user(user: UserSchema) -> UserSchema:
    """
    Create a new user and persist it to the database
    """
    # Convert Pydantic model to SQLAlchemy model
    db_user = UserModel(
        email=user.email,
        name=user.name,
        role=user.role
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
    
    return user

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
