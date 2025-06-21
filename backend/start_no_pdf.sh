#!/bin/bash
echo "Starting LegalDoc API..."
echo "Skipping PDF processing to save memory..."
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 