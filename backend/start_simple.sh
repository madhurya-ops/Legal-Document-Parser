#!/bin/bash
echo "Starting LegalDoc API..."
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 