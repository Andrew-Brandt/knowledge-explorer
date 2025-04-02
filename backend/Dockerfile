# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (for psycopg2 and gcc)
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Copy the app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run using Gunicorn and app factory
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:create_app()"]
