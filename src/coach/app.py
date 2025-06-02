# src/coach/app.py

from flask import Flask
from src.coach.routes.wod_routes import wod_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(wod_bp)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "UP"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)