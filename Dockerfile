FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --locked --no-install-project

COPY src/ ./src/

RUN uv sync --locked --no-editable

ENV PATH="/app/.venv/bin:$PATH"

ENV PORT=10000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} whatsapp_service_002.app:app"]

