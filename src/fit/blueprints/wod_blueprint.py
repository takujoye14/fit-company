from flask import Blueprint, jsonify
from ..services.rabbitmq_service import rabbitmq_service
from ..models_db import UserModel
from ..database import db_session

wod_bp = Blueprint('wod', __name__)

@wod_bp.route('/generate_wods', methods=['POST'])
def generate_wods():
    """
    Loop through all users and publish a WOD creation job to the queue.
    """
    db = db_session()
    try:
        users = db.query(UserModel).all()


        
        for user in users:
            message = {
                "user_email": user.email
            }
            rabbitmq_service.publish_message(message)
        return jsonify({"status": "success", "message": f"WOD jobs created for {len(users)} users"}), 200
    except Exception as e:
        print(f"Error creating WOD jobs: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()
