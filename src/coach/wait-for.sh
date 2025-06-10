#!/bin/bash

set -e

RABBITMQ_HOST=${RABBITMQ_HOST:-rabbitmq}
RABBITMQ_USER=${RABBITMQ_DEFAULT_USER:-rabbit}
RABBITMQ_PASS=${RABBITMQ_DEFAULT_PASS:-docker}
QUEUE_NAME=${QUEUE_NAME:-createWodQueue}

echo "Waiting for RabbitMQ to be available..."

# Wait for RabbitMQ port to be reachable
until nc -z $RABBITMQ_HOST 5672; do
  echo "Waiting for RabbitMQ at $RABBITMQ_HOST:5672..."
  sleep 2
done

echo "RabbitMQ is up. Waiting for queue '$QUEUE_NAME' to exist..."

# Wait for the queue to exist
while true; do
  if rabbitmqadmin -H $RABBITMQ_HOST -u $RABBITMQ_USER -p $RABBITMQ_PASS list queues name | grep -q "$QUEUE_NAME"; then
    echo "Queue '$QUEUE_NAME' exists!"
    break
  else
    echo "Queue '$QUEUE_NAME' not yet found, retrying..."
    sleep 2
  fi
done

echo "Starting consumer..."
exec python -m src.coach.wod_consumer
