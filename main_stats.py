#!/usr/bin/env python
import threading
from src.stats.app import run_app
from src.stats.consumer import StatsConsumer

def start_consumer():
    """Start the RabbitMQ consumer in a separate thread"""
    print("start_consumer called")
    consumer = StatsConsumer()
    consumer_thread = threading.Thread(target=consumer.start_consuming, daemon=True)
    consumer_thread.start()

if __name__ == "__main__":
    start_consumer()
    run_app()
