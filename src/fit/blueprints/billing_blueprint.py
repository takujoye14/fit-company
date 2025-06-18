from flask import Blueprint, request, jsonify
import pika
import json

billing_bp = Blueprint("billing", __name__)

@billing_bp.route("/subscribe", methods=["POST"])
def subscribe():
    try:
        data = request.get_json()
        email = data.get("email")
        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
        channel = connection.channel()
        channel.queue_declare(queue="premium_status_queue", durable=True)

        message = {"email": email, "is_premium": True}
        channel.basic_publish(
            exchange='',
            routing_key='premium_status_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # make message persistent
            )
        )
        connection.close()

        return jsonify({"message": f"{email} subscribed to premium successfully!"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to subscribe", "details": str(e)}), 500
