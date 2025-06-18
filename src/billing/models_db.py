from dataclasses import dataclass

@dataclass
class Subscription:
    user_id: str
    is_premium: bool
