FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml pyproject.toml
RUN uv pip install -e . --system --no-cache

COPY app/ /app/
