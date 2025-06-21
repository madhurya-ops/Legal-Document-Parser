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

# Create production start script with lightweight PDF processing
RUN echo '#!/bin/bash\n\
echo "Starting LegalDoc API..."\n\
echo "Processing PDFs with lightweight mode..."\n\
python embeddings/embed_pdfs_lightweight.py || echo "PDF processing failed, continuing..."\n\
echo "Starting FastAPI server..."\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1' > /app/start.sh && chmod +x /app/start.sh

# Expose FastAPI port
EXPOSE 8000

# Start the application
CMD ["/app/start.sh"]
