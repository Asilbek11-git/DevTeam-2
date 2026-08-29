# ==============================================================================
# DevTeam SaaS - Production Dockerfile
# ==============================================================================

FROM python:3.12-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    PORT=3000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose container port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/api/v1/health/ || exit 1

# Start Gunicorn server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:3000", "--workers", "4", "--threads", "2", "--timeout", "120"]
