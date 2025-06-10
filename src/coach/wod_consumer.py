import time
import os
import json
import pika
import random
from src.coach.fitness_coach_service import request_wod
from src.coach.database import db_session
from src.coach.models_db import GeneratedWODModel
from src.coach.models_dto import CreateWodMessage

class WodConsumer:
    def __init__(self):
        self.queue_name = "createWodQueue"
        self.dead_letter_queue = f"{self.queue_name}-dead"

        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self.rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER", "rabbit")
        self.rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS", "docker")

        self.connection = None
        self.channel = None

        # Retry logic
        max_retries = 5
        retry_delay = 5  # seconds

        for attempt in range(1, max_retries + 1):
            try:
                print(f"🚀 Attempting to connect to RabbitMQ (try {attempt}/{max_retries})...")
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.rabbitmq_host,
                        credentials=pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_pass)
                    )
                )
                self.channel = self.connection.channel()
                self.channel.basic_qos(prefetch_count=1)
                print("✅ Connected to RabbitMQ!")
                break
            except pika.exceptions.AMQPConnectionError as e:
                print(f"⚠️ Connection attempt {attempt} failed: {e}")
                if attempt < max_retries:
                    time.sleep(retry_delay)
                else:
                    print("❌ Failed to connect to RabbitMQ after multiple attempts. Exiting.")
                    raise

    def start(self):
        print("👀 Consumer started and waiting for messages.")
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback
        )
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        session = db_session()
        try:
            message = json.loads(body)

            # Validate message
            validated_message = CreateWodMessage(**message)
            user_email = validated_message.user_email
            attempt = validated_message.attempt

            # Simulate 20% random failure
            if random.random() < 0.2:
                raise Exception("Simulated random failure for testing retries.")

            exercises_with_muscles = request_wod(user_email)
            for exercise, muscle_groups in exercises_with_muscles:
                suggested_weight = random.uniform(5.0, 50.0)
                suggested_reps = random.randint(8, 15)
                generated_wod = GeneratedWODModel(
                    user_email=user_email,
                    exercise_name=exercise.name,
                    suggested_weight=suggested_weight,
                    suggested_reps=suggested_reps
                )
                session.add(generated_wod)
            session.commit()
            print(f"✅ WOD generated for user: {user_email}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"❌ Error processing message: {str(e)}")
            session.rollback()
            attempt = message.get("attempt", 0) + 1
            message["attempt"] = attempt

            if attempt < 3:
                self.channel.basic_publish(
                    exchange='',
                    routing_key=self.queue_name,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
                print(f"🔄 Requeued message for user: {message.get('user_email')} (attempt {attempt})")
            else:
                self.channel.basic_publish(
                    exchange='dlx',
                    routing_key=self.dead_letter_queue,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
                print(f"💀 Sent message to DLQ for user: {message.get('user_email')} (attempt {attempt})")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        finally:
            session.close()

def start_consumer():
    consumer = WodConsumer()
    consumer.start()

if __name__ == "__main__":
    start_consumer()
