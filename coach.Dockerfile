# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files needed for uv sync
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync

# Activate .venv globally
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install curl and netcat-openbsd (for healthcheck / wait-for)
RUN apt-get update && \
    apt-get install -y curl netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Copy the entire application source code
COPY src/coach/ /app/src/coach/
COPY main_coach.py /app/main_coach.py

ENV FLASK_ENV=development

EXPOSE 5000

CMD ["uv", "run", "main_coach.py"]
