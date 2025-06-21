# Lightweight PDF Processing Guide

## Overview
This solution provides **limited but functional PDF processing** that works within Render's free tier memory constraints (512MB).

## What It Does

### ✅ **Processes PDFs Within Limits:**
- **File Size**: Max 3MB per PDF (free tier) / 10MB (paid tier)
- **Pages**: Max 5 pages per PDF (free tier) / 20 pages (paid tier)
- **Chunks**: Max 50 total chunks (free tier) / 200 chunks (paid tier)
- **Chunks per Page**: Max 5 chunks per page (free tier) / 15 chunks (paid tier)

### ✅ **Memory-Efficient Processing:**
- **Small chunks**: 150 characters (free) / 250 characters (paid)
- **Batch processing**: 5 documents at a time (free) / 15 documents (paid)
- **Garbage collection**: After each page and batch
- **Lightweight models**: Uses smallest possible embedding models

### ✅ **Graceful Degradation:**
- Skips large PDFs automatically
- Limits pages per PDF
- Creates empty index if processing fails
- Continues startup even if PDF processing fails

## Configuration

### Free Tier Settings (Conservative)
```python
RENDER_FREE_TIER = {
    'MAX_PDF_SIZE_MB': 3,      # 3MB max per PDF
    'MAX_PAGES': 5,            # 5 pages max per PDF
    'MAX_CHUNKS': 50,          # 50 total chunks
    'MAX_CHUNKS_PER_PAGE': 5,  # 5 chunks per page
    'CHUNK_SIZE': 150,         # 150 characters per chunk
    'BATCH_SIZE': 5            # 5 documents per batch
}
```

### Paid Tier Settings (More Generous)
```python
RENDER_PAID_TIER = {
    'MAX_PDF_SIZE_MB': 10,     # 10MB max per PDF
    'MAX_PAGES': 20,           # 20 pages max per PDF
    'MAX_CHUNKS': 200,         # 200 total chunks
    'MAX_CHUNKS_PER_PAGE': 15, # 15 chunks per page
    'CHUNK_SIZE': 250,         # 250 characters per chunk
    'BATCH_SIZE': 15           # 15 documents per batch
}
```

## How to Use

### 1. Deploy with Lightweight Processing
The current configuration uses lightweight PDF processing by default:

**Render Start Command:**
```bash
cd backend && python embeddings/embed_pdfs_lightweight.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
```

**Docker:**
```dockerfile
CMD ["/app/start.sh"]  # Uses lightweight processing
```

### 2. Adjust Limits (Optional)
Edit `backend/pdf_config.py` to change limits:

```python
# For more generous limits (if you upgrade to paid tier)
config = get_config('paid')  # Change from 'free' to 'paid'
```

### 3. Monitor Processing
The script will show:
- Which PDFs are being processed
- Which PDFs are skipped (and why)
- How many chunks are created
- Memory usage warnings

## Example Output

```
Found 3 PDFs.
Using limits: 3MB max, 5 pages, 50 chunks
Processing small_contract.pdf (1.2MB)...
Processing medium_contract.pdf (4.1MB)...
Skipping large_contract.pdf - too large (8.5MB > 3MB)
Successfully processed 45 chunks from 2 PDFs
Lightweight FAISS index saved to index
Index contains 45 chunks with 384-dimensional embeddings
```

## What Gets Processed

### ✅ **Will Process:**
- Small PDFs (< 3MB for free tier)
- First 5 pages of each PDF
- Up to 50 total text chunks
- Simple text content

### ❌ **Will Skip:**
- Large PDFs (> 3MB)
- PDFs with many pages (keeps first 5)
- Complex PDFs with images/tables
- PDFs that cause memory errors

## Memory Usage

### Expected Memory Usage:
- **Startup**: ~200-300MB
- **PDF Processing**: ~400-450MB (within 512MB limit)
- **Runtime**: ~250-350MB

### Memory Optimization:
- Processes one PDF at a time
- Clears memory after each page
- Uses smallest possible embedding models
- Batches embedding creation

## Troubleshooting

### Still Getting Memory Errors?
1. **Reduce limits** in `pdf_config.py`:
   ```python
   MAX_PDF_SIZE_MB = 2  # Reduce from 3 to 2
   MAX_PAGES = 3        # Reduce from 5 to 3
   MAX_CHUNKS = 30      # Reduce from 50 to 30
   ```

2. **Skip PDF processing entirely**:
   ```bash
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
   ```

3. **Upgrade to paid tier** for more memory

### Need More PDF Processing?
1. **Upgrade to paid tier** and use `get_config('paid')`
2. **Process PDFs locally** and upload the index
3. **Use a separate service** for heavy PDF processing

## Benefits

### ✅ **Advantages:**
- **Works on free tier**: Stays within 512MB limit
- **Functional**: Provides basic PDF search capabilities
- **Configurable**: Easy to adjust limits
- **Robust**: Handles errors gracefully
- **Fast**: Quick startup with limited processing

### ⚠️ **Limitations:**
- **Limited PDF size**: Only small PDFs
- **Limited pages**: Only first few pages
- **Basic processing**: No complex text extraction
- **Limited chunks**: Reduced search accuracy

## Next Steps

1. **Deploy with current settings** (free tier limits)
2. **Test with small PDFs** (< 3MB, < 5 pages)
3. **Monitor memory usage** during deployment
4. **Adjust limits** if needed
5. **Upgrade to paid tier** for more generous limits

This solution gives you **functional PDF processing** while staying within Render's free tier constraints! 