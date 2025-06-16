import os
import pika
import json
import logging
from datetime import datetime

from .models_db import WorkoutStat, SessionLocal
from pydantic import ValidationError
from .queue_messages import WorkoutPerformedMessage

logger = logging.getLogger(__name__)
logging.getLogger("pika").setLevel(logging.WARNING)

class StatsConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = "workout.performed"
        self.queue_name = "stats.workout.performed"

    def connect(self):
        credentials = pika.PlainCredentials(
            username=os.getenv("RABBITMQ_DEFAULT_USER", "rabbit"),
            password=os.getenv("RABBITMQ_DEFAULT_PASS", "docker")
        )
        parameters = pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST", "rabbitmq"),
            port=5672,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, exchange_type="fanout")

        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange=self.exchange, queue=queue_name)
        self.queue_name = queue_name

        logger.info(f"Connected and bound to exchange '{self.exchange}'")

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_message,
            auto_ack=False
        )

    def process_message(self, ch, method, properties, body):
        try:
            logger.debug(f"Received message: {body}")
            data = json.loads(body)
            message = WorkoutPerformedMessage(**data)

            db = SessionLocal()
            stat = WorkoutStat(
                workout_id=message.workout_id,
                user_email=message.user_email,
                performed_at=message.performed_at,
                exercise_ids=message.exercise_ids
            )
            db.add(stat)
            db.commit()
            db.close()

            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Stored workout stats for user {message.user_email}")

        except (json.JSONDecodeError, ValidationError) as e:
            logger.error(f"Invalid message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start(self):
        self.connect()
        logger.info("Starting stats consumer...")
        self.channel.start_consuming()
