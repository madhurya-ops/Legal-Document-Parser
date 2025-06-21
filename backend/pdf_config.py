# PDF Processing Configuration
# Adjust these values based on your deployment environment

# Memory Limits
MAX_PDF_SIZE_MB = 5  # Maximum PDF file size to process
MAX_PAGES = 10  # Maximum pages per PDF to process
MAX_CHUNKS = 100  # Maximum total text chunks across all PDFs
MAX_CHUNKS_PER_PAGE = 10  # Maximum chunks per page

# Processing Settings
CHUNK_SIZE = 200  # Characters per text chunk
CHUNK_OVERLAP = 20  # Overlap between chunks
BATCH_SIZE = 10  # Documents to process in each batch

# Model Settings
EMBEDDING_MODEL = 'paraphrase-MiniLM-L3-v2'  # Lightweight model
FALLBACK_MODEL = 'all-MiniLM-L6-v2'  # Fallback if primary fails

# Render Free Tier Settings (Conservative)
RENDER_FREE_TIER = {
    'MAX_PDF_SIZE_MB': 3,
    'MAX_PAGES': 5,
    'MAX_CHUNKS': 50,
    'MAX_CHUNKS_PER_PAGE': 5,
    'CHUNK_SIZE': 150,
    'BATCH_SIZE': 5
}

# Render Paid Tier Settings (More generous)
RENDER_PAID_TIER = {
    'MAX_PDF_SIZE_MB': 10,
    'MAX_PAGES': 20,
    'MAX_CHUNKS': 200,
    'MAX_CHUNKS_PER_PAGE': 15,
    'CHUNK_SIZE': 250,
    'BATCH_SIZE': 15
}

def get_config(tier='free'):
    """Get configuration based on deployment tier"""
    if tier == 'paid':
        return RENDER_PAID_TIER
    else:
        return RENDER_FREE_TIER 