-- Create user_exercise_history table
CREATE TABLE IF NOT EXISTS user_exercise_history (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR NOT NULL REFERENCES users(email),
    exercise_id INTEGER REFERENCES exercises(id),
    date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_exercise_history_user_date 
ON user_exercise_history(user_email, date);
