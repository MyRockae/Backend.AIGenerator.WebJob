# Stage 1: Build Stage
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update -qq && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Stage 2: Final Image
FROM python:3.9-slim
WORKDIR /app

# Install runtime dependencies (libpq for PostgreSQL)
RUN apt-get update -qq && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages and Gunicorn
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Copy application code
COPY . /app/


# Collect static files
#RUN python manage.py collectstatic --noinput

# Set environment variables
ENV PORT=8000
EXPOSE $PORT

# Use shell form to resolve $PORT dynamically
CMD gunicorn BackendGeneratorWebAPI.wsgi:application --bind 0.0.0.0:8000 --workers=3 --timeout 120
