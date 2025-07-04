# Use Python slim image for smaller footprint
FROM python:3.11-slim

WORKDIR /app

# Install essential system dependencies including curl for health checks
RUN apt-get update && apt-get install -y \
    build-essential \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

# Copy application code
COPY . .

# Create optimized start script with memory limits
RUN echo '#!/bin/bash\n\
echo "Starting LegalDoc API with memory optimization..."\n\
export PYTHONOPTIMIZE=1\n\
export PYTHONDONTWRITEBYTECODE=1\n\
export PYTHONUNBUFFERED=1\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --limit-concurrency 5 --limit-max-requests 500 --backlog 10' > /app/start.sh \
    && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Set environment variables for memory optimization
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONOPTIMIZE=1
ENV PYTHONHASHSEED=0

# Start application
CMD ["/app/start.sh"]
