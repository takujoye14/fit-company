from .database import get_db_connection
from .models_db import Subscription
import requests
import os

def notify_monolith(email: str):
    MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:5000")
    try:
        requests.post(f"{MONOLITH_URL}/api/users/set-premium", json={"email": email})
    except Exception as e:
        print(f"Failed to notify monolith: {e}")

def mark_user_premium(email: str) -> None:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO subscriptions (email, is_premium) VALUES (%s, TRUE) "
        "ON CONFLICT (email) DO UPDATE SET is_premium = TRUE",
        (email,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"[Billing] Marking user {email} as premium (simulated)")

def is_user_premium(email: str) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT is_premium FROM subscriptions WHERE email = %s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else False
