from flask import Flask, request, jsonify
from pydantic import ValidationError

import os

app = Flask(__name__)

# Register blueprints

@app.route("/health")
def health():
    return {"status": "UP"}


def run_app():
    """Entry point for the application script"""
    # Initialize the database before starting the app
    # init_db()
    
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    run_app()

