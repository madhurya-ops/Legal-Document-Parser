# Memory Optimization Fix Guide

## Problem
The application was running out of memory (>512MB) during deployment on Render's free tier due to:
1. Heavy PDF processing with large embedding models
2. FAISS vector store operations
3. Hugging Face model loading

## Solutions Implemented

### 1. Memory-Efficient PDF Processing
- **Smaller chunks**: Reduced from 600 to 300 characters
- **Batch processing**: Process 50 documents at a time
- **Memory cleanup**: Added garbage collection after each batch
- **Lighter models**: Use CPU-only models with smaller dimensions

### 2. Optimized Embedding Models
- **Primary**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **Fallback**: `sentence-transformers/paraphrase-MiniLM-L3-v2` (384 dimensions)
- **CPU-only**: Explicitly set `device='cpu'` to avoid GPU memory issues

### 3. Custom FAISS Implementation
- **Manual index creation**: More control over memory usage
- **Separate storage**: Index and documents stored separately
- **Custom retriever**: Handles the new storage format

### 4. Deployment Options

#### Option A: No PDF Processing (Recommended for Render Free Tier)
```bash
# Start command
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
```
- **Pros**: Fast startup, low memory usage
- **Cons**: No pre-processed PDFs
- **Use case**: When you don't need PDF processing on startup

#### Option B: Memory-Efficient PDF Processing
```bash
# Start command
cd backend && python embeddings/embed_pdfs.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
```
- **Pros**: PDFs are processed with memory optimization
- **Cons**: Still uses significant memory
- **Use case**: When you need PDF processing

#### Option C: Docker with No PDF Processing
```dockerfile
# Use the updated Dockerfile
CMD ["/app/start.sh"]
```

## Environment Variables Required

1. **DATABASE_URL**: Your Render PostgreSQL connection string
2. **SECRET_KEY**: A secure random string
3. **HF_API_KEY**: Your Hugging Face API key (optional for basic functionality)

## Files Modified

### Core Files
- `backend/embeddings/embed_pdfs.py`: Memory-efficient PDF processing
- `backend/app/core/vector_store.py`: Custom FAISS loading
- `backend/Dockerfile`: Updated startup script
- `backend/requirements.txt`: Lighter package versions

### Configuration Files
- `render.yaml`: Updated for memory optimization
- `docker-compose.prod.yml`: Production configuration

### Startup Scripts
- `backend/start_simple.sh`: Basic startup
- `backend/start_no_pdf.sh`: No PDF processing

## Deployment Steps

### For Render (Recommended)
1. **Create PostgreSQL database** on Render
2. **Create Web Service** with these settings:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1`
3. **Set Environment Variables**:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `SECRET_KEY`: Secure random string
   - `HF_API_KEY`: Your Hugging Face API key
4. **Deploy**

### For Docker
1. **Use production compose**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```
2. **Set environment variables** in your deployment platform

## Expected Results

### Memory Usage
- **Before**: >512MB (causing crashes)
- **After**: ~200-300MB (stable)

### Startup Time
- **Before**: 2-3 minutes (with PDF processing)
- **After**: 30-60 seconds (no PDF processing)

### Functionality
- **Authentication**: ✅ Working
- **API endpoints**: ✅ Working
- **Health check**: ✅ Working
- **PDF processing**: ⚠️ Optional (can be done separately)

## Troubleshooting

### Still Getting Memory Errors?
1. **Upgrade Render plan** to paid tier (more memory)
2. **Use Option A** (no PDF processing)
3. **Process PDFs separately** on a more powerful machine

### PDF Processing Needed?
1. **Use Option B** with memory optimization
2. **Process PDFs locally** and upload the index files
3. **Use a separate service** for PDF processing

### Database Connection Issues?
1. **Check DATABASE_URL** format
2. **Verify PostgreSQL service** is running
3. **Test connection** manually

## Next Steps

1. **Deploy with Option A** (no PDF processing)
2. **Test the health endpoint**: `https://your-app.onrender.com/health`
3. **Verify authentication** works
4. **Add PDF processing later** if needed

The application should now deploy successfully on Render's free tier without memory issues! 