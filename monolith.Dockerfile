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

# Copy the entire application source code
COPY src/fit/ /app/src/fit/
COPY main_monolith.py /app/main_monolith.py
COPY src/fit/cron_job.py /app/src/fit/cron_job.py

ENV FLASK_ENV=development

EXPOSE 5000

CMD ["uv", "run", "main_monolith.py"]
