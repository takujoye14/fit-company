from .database import get_db_session
from .models_db import Subscription
import requests
import os

def notify_monolith(email: str, is_premium: bool = True):
    MONOLITH_URL = os.getenv("MONOLITH_URL", "http://monolith:5000")
    try:
        requests.post(
            f"{MONOLITH_URL}/users/set-premium",
            json={"email": email, "is_premium": is_premium}
        )
    except Exception as e:
        print(f"Failed to notify monolith: {e}")


def mark_user_premium(email: str) -> None:
    db = get_db_session()
    sub = db.query(Subscription).filter_by(email=email).first()
    if sub:
        sub.is_premium = True
    else:
        sub = Subscription(email=email, is_premium=True)
        db.add(sub)
    db.commit()
    db.close()
    print(f"[Billing] Marked user {email} as premium.")

def is_user_premium(email: str) -> bool:
    db = get_db_session()
    sub = db.query(Subscription).filter_by(email=email).first()
    db.close()
    return sub.is_premium if sub else False

def cancel_user_subscription(email: str) -> bool:
    """
    Cancel the user's premium subscription.
    Returns True if cancelled, False if already not premium.
    """
    db = get_db_session()
    sub = db.query(Subscription).filter_by(email=email).first()
    if sub and sub.is_premium:
        sub.is_premium = False
        db.commit()
        db.close()
        print(f"[Billing] Cancelled premium subscription for {email}")
        return True
    db.close()
    return False

