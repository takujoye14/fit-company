# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY src/stats /app/src/stats
COPY main_stats.py /app/main_stats.py

ENV FLASK_ENV=development
EXPOSE 5002

CMD ["uv", "run", "main_stats.py"]
