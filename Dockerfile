# LagnaMaster — single image used by both api and ui services
FROM python:3.12-slim

# pyswisseph requires gcc/g++ to compile the C extension
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies before copying source (layer-cache friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/      src/
COPY tests/    tests/
COPY ephe/     ephe/

# Pre-create runtime directories so the volume mount owns them
RUN mkdir -p data

ENV PYTHONPATH=/app

# Default: API. Overridden in docker-compose.yml per service.
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
