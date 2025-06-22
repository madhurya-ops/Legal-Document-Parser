# PDF Processing Configuration
# Adjust these values based on your deployment environment

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
    return RENDER_PAID_TIER if tier == 'paid' else RENDER_FREE_TIER 