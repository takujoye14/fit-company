import os
import psycopg2
import requests

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@billing-db:5432/billing")
MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:5000")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def get_user_by_email(email: str):
    """
    Contacts the monolith to verify the user exists based on email.
    """
    try:
        response = requests.post(
            f"{MONOLITH_URL}/api/users/lookup",
            json={"email": email},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()  # should return user data (e.g., email, name, role, etc.)
        return None
    except Exception as e:
        print(f"[Billing] Error contacting monolith for user lookup: {e}")
        return None
