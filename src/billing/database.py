import os
from sqlalchemy.orm import Session
import requests
from .models_db import SessionLocal

MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:5000")

def get_db_session() -> Session:
    return SessionLocal()

def get_user_by_email(email: str):
    try:
        response = requests.post(
            f"{MONOLITH_URL}/users/lookup",
            json={"email": email},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"[Billing] Error contacting monolith for user lookup: {e}")
        return None
