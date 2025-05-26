from flask import Flask
from .routes.user_routes import user_bp
from .routes.auth_routes import auth_bp
from .routes.profile_routes import profile_bp
from .routes.fitness_routes import fitness_bp
from .database import init_db
from .services.fitness_data_init import init_fitness_data

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(fitness_bp)

@app.route("/health")
def health():
    return {"status": "UP"}

def run_app():
    # Initialize the database and seed fitness data
    init_db()
    init_fitness_data()
    app.run(host="0.0.0.0", port=5001, debug=True)

if __name__ == "__main__":
    run_app()
