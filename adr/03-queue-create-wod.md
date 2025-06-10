- We added a main queue (createWodQueue) to handle the failed messages cleanly.
This way, if a WOD generation fails too many times, it goes to the dead-letter queue for later analysis.
- We updated the Docker Compose and Health Checks
- We used Docker Compose to manage our services (Monolith, Coach, RabbitMQ, Databases) and we added depends_on to make the wod_consumer not start until the RabbitMQ service is reeady
- Inside the consumer, we implemented logic that retries a failed message up to 3 times before moving it to the dead-letter queue.
    This helps to handle the temporary issues without dropping the message entirely.
- Finnaly we wrote a separate cron_job.py script to automatically call the API endpoint every hour to generate WODs for all users.
This makes the system more dynamic and avoids having to manually trigger the endpoint.

Suggestons to streghten the system even more:
  - Add token-based authentication (or mTLS) between the different services
  - We could integrate tools like Prometheus or Grafana to monitor queues, processing times, and system health.

  - Add a check to make sure that if the same message is processed more than once, it doesn’t create duplicate WODs. We could use a unique ID per job to make this work.