# Use a lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt-get/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and configuration files
COPY src/ ./src/
COPY configs/ ./configs/
COPY tests/ ./tests/

# Create directory for persistent data mounts
RUN mkdir -p /app/data/raw /app/data/processed

# Default command runs the ingestion module
CMD ["python", "src/ingest.py"]