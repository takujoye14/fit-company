import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@billing-db:5432/billing")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def get_user_by_email(email: str):
    dummy_users = {
        "john@example.com": {"id": "user123"},
        "jane@example.com": {"id": "user456"}
    }
    return dummy_users.get(email)
