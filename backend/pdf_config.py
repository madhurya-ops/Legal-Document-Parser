# PDF Processing Configuration - Memory Optimized
# Conservative settings for 512MB RAM deployment while preserving functionality

# Render Free Tier Settings (Conservative but functional)
RENDER_FREE_TIER = {
    'MAX_PDF_SIZE_MB': 1,      # Increased from 0.5MB for better functionality
    'MAX_PAGES': 3,            # Keep at 3 for memory efficiency
    'MAX_CHUNKS': 20,          # Increased from 10 for better coverage
    'MAX_CHUNKS_PER_PAGE': 3,  # Increased from 2 for better text processing
    'CHUNK_SIZE': 100,         # Increased from 60 for better context
    'BATCH_SIZE': 3            # Increased from 2 for better performance
}

# Render Paid Tier Settings (More generous)
RENDER_PAID_TIER = {
    'MAX_PDF_SIZE_MB': 3,      # Increased from 2MB
    'MAX_PAGES': 8,            # Increased from 5
    'MAX_CHUNKS': 80,          # Increased from 50
    'MAX_CHUNKS_PER_PAGE': 6,  # Increased from 4
    'CHUNK_SIZE': 150,         # Increased from 100
    'BATCH_SIZE': 6            # Increased from 4
}

def get_config(tier='free'):
    """Get configuration based on deployment tier"""
    return RENDER_PAID_TIER if tier == 'paid' else RENDER_FREE_TIER # update Sun Jul  6 02:55:00 IST 2025
# update Sun Jul  6 02:56:34 IST 2025
