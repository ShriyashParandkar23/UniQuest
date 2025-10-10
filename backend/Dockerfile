# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_ENVIRONMENT=prod

# Set work directory
WORKDIR /app

# Install system dependencies (removed MySQL dependencies)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        pkg-config \
        build-essential \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN addgroup --system django \
    && adduser --system --group django

# Create data directory and set permissions
RUN mkdir -p /data && chown -R django:django /data
RUN mkdir -p /app/staticfiles && chown -R django:django /app/staticfiles
RUN mkdir -p /app/media && chown -R django:django /app/media
RUN mkdir -p /app/db && chown -R django:django /app/db

# Change to non-root user
USER django

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/healthz/ || exit 1

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "wsgi:application"]