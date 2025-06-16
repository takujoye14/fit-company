FROM python:3.11-slim

WORKDIR /app

COPY ./src/stats /app/src/stats

RUN pip install flask psycopg2-binary pika sqlalchemy

ENV PYTHONPATH=/app

CMD ["python", "src/stats/app.py"]