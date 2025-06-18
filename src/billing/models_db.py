from dataclasses import dataclass

@dataclass
class Subscription:
    email: str
    is_premium: bool
