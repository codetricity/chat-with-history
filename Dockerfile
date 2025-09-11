FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    PORT=8000

RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential \
  && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
# Copy dependency files
COPY pyproject.toml uv.lock* ./
# Install dependencies (no dev dependencies for production)
RUN uv sync --frozen --no-dev

COPY . .
EXPOSE 8000

# Create startup script that handles initialization
RUN echo '#!/bin/bash\nset -e\n\n# Run database initialization and hybrid search setup\nuv run python startup.py\n\n# Start the FastAPI application\nuv run uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*"\n' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
