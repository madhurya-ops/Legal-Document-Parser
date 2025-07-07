#!/bin/bash

echo "Starting LegalDoc API for Render deployment..."

# Skip PDF processing on Render free tier to avoid memory issues
echo "Skipping PDF processing to stay within memory limits..."
echo "PDFs can be uploaded and processed via the web interface"

# Start FastAPI server with single worker
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 # update Sun Jul  6 02:56:34 IST 2025
