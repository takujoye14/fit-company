import pika
import json
import threading

premium_users = set()

def run_premium_status_consumer():
    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            email = message.get("email")
            is_premium = message.get("is_premium")

            if is_premium and email:
                premium_users.add(email)
                print(f"[✔] Added premium user: {email}")
            elif not is_premium and email:
                premium_users.discard(email)
                print(f"[✘] Removed premium user: {email}")
        except Exception as e:
            print(f"[!] Failed to process premium message: {e}")

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='premium_status_queue', durable=True)

        channel.basic_consume(
            queue='premium_status_queue',
            on_message_callback=callback,
            auto_ack=True
        )

        print("[🟢] Listening for premium status updates...")
        channel.start_consuming()
    except Exception as e:
        print(f"[!] Premium status consumer crashed: {e}")
