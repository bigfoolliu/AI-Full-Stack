FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* && \
    arch="$(dpkg --print-architecture)" && \
    case "$arch" in \
        arm64) url='https://github.com/tianon/gosu/releases/download/1.17/gosu-arm64' ;; \
        amd64) url='https://github.com/tianon/gosu/releases/download/1.17/gosu-amd64' ;; \
    esac && \
    curl -L -o /usr/local/bin/gosu "$url" && \
    chmod +x /usr/local/bin/gosu

RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app/data /app/uploads && \
    chmod 777 /app/data /app/uploads

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
