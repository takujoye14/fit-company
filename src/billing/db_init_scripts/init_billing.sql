CREATE TABLE IF NOT EXISTS subscriptions (
    user_id TEXT PRIMARY KEY,
    is_premium BOOLEAN DEFAULT FALSE
);
