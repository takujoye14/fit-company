CREATE TABLE IF NOT EXISTS subscriptions (
    email TEXT PRIMARY KEY,
    is_premium BOOLEAN DEFAULT FALSE
);