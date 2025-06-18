from database import get_db_connection
from models_db import Subscription
import requests

def notify_monolith(user_id: str):
    MONOLITH_URL = os.getenv("MONOLITH_URL", "http://localhost:12100/")
    try:
        requests.post(f"{MONOLITH_URL}/api/users/set-premium", json={"user_id": user_id})
    except Exception as e:
        print(f"Failed to notify monolith: {e}")

def mark_user_premium(user_id: str) -> None:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO subscriptions (user_id, is_premium) VALUES (%s, TRUE) "
        "ON CONFLICT (user_id) DO UPDATE SET is_premium = TRUE",
        (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"[Billing] Marking user {user_id} as premium (simulated)")


def is_user_premium(user_id: str) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT is_premium FROM subscriptions WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else False


def notify_monolith(user_id: str):
    MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:5000")
    try:
        requests.post(f"{MONOLITH_URL}/api/users/set-premium", json={"user_id": user_id})
    except Exception as e:
        print(f"Failed to notify monolith: {e}")