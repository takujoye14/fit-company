from src.billing.models_db import init_db
from src.billing.app import app

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
