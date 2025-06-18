import pika
import os
import logging
import json
from pydantic import ValidationError
from .queue_messages import WorkoutPerformedMessage
from .models_db import SessionLocal, WorkoutStat

logger = logging.getLogger(__name__)
logging.getLogger("pika").setLevel(logging.DEBUG)

class StatsConsumer:
    def __init__(self):
        self.queue_name = "workoutCompleted"
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        credentials = pika.PlainCredentials(
            os.getenv("RABBITMQ_DEFAULT_USER", "rabbit"),
            os.getenv("RABBITMQ_DEFAULT_PASS", "docker")
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

        # 1. Declare the fanout exchange
        self.channel.exchange_declare(exchange="workout.performed", exchange_type="fanout")

        # 2. Declare the queue (durable)
        self.channel.queue_declare(queue=self.queue_name, durable=True)

        # 3. Bind the queue to the exchange
        self.channel.queue_bind(exchange="workout.performed", queue=self.queue_name)

    

    def callback(self, ch, method, properties, body):
        try:
            logger.info(f"Message received: {body.decode()}")
            print(f"Message received: {body.decode()}")
            message = WorkoutPerformedMessage.model_validate_json(body.decode())

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
            print("saved to db")
        except ValidationError as e:
            logger.error(f"Validation failed: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"Unhandled error: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


    def start_consuming(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback
        )
        print(f"Started consuming from queue '{self.queue_name}'")
        logger.info(f"Started consuming from queue '{self.queue_name}'")
        self.channel.start_consuming()