# Memory Optimization Guide for Render Deployment

## Issues Fixed

1. **Out of Memory Error**: App was using over 512MB and getting killed
2. **Deprecated LangChain Imports**: Updated to use `langchain_community`
3. **FAISS Loading Errors**: Added error handling and fallback
4. **Port Detection**: Simplified startup process

## Changes Made

### 1. Updated Imports
- Changed `langchain.document_loaders` → `langchain_community.document_loaders`
- Changed `langchain.vectorstores` → `langchain_community.vectorstores`

### 2. Added Error Handling
- Vector store loading now has fallback mechanisms
- PDF processing won't crash the entire app
- Graceful degradation when index doesn't exist

### 3. Memory Optimization
- Reduced workers to 1 (`--workers 1`)
- Added numpy version constraint
- Simplified startup process

## Deployment Options

### Option 1: Simple Deployment (Recommended)
Use this start command in Render:
```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
```

### Option 2: With PDF Processing
If you need PDF processing, use:
```bash
cd backend && python embeddings/embed_pdfs.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
```

### Option 3: Docker Deployment
Use the updated `docker-compose.prod.yml` with environment variables.

## Environment Variables Required

1. **DATABASE_URL**: Your Render PostgreSQL connection string
2. **SECRET_KEY**: A secure random string
3. **HF_API_KEY**: Your Hugging Face API key

## Troubleshooting

### Memory Issues
- The app now uses single worker to reduce memory usage
- PDF processing is optional and won't crash the app
- Vector store has fallback mechanisms

### Port Issues
- Make sure to use `$PORT` environment variable
- App listens on `0.0.0.0:$PORT`

### Database Issues
- Ensure `DATABASE_URL` is correctly set
- Check that PostgreSQL service is running

## Next Steps

1. **Update your Render service** with the new start command
2. **Set environment variables** (DATABASE_URL, SECRET_KEY, HF_API_KEY)
3. **Redeploy** the application
4. **Test the health endpoint**: `https://your-app.onrender.com/health`

## Expected Behavior

- App should start without memory errors
- Health endpoint should return `{"status": "healthy", "service": "LegalDoc API"}`
- Vector store will work with fallback if index doesn't exist
- PDF processing is optional and won't block startup 