# Use a slim Python image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y build-essential postgresql-client && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Create wait script
RUN echo '#!/bin/bash\n\
until pg_isready -h db -p 5432 -U postgres; do\n\
  echo "Waiting for database..."\n\
  sleep 2\n\
done\n\
echo "Database is ready!"\n\
python embeddings/embed_pdfs.py\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000' > /app/start.sh && chmod +x /app/start.sh

# Expose FastAPI port
EXPOSE 8000

# Start with wait script
CMD ["/app/start.sh"]
