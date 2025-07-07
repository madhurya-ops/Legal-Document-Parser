import logging
import sys

def setup_logging(level=logging.INFO):
    """Configure basic logging"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        stream=sys.stdout
    )

def get_logger(name: str):
    """Get logger instance"""
    return logging.getLogger(name)

# Example of how to initialize it in main.py or a startup script
# setup_logging() # update Sun Jul  6 02:54:59 IST 2025
# update Sun Jul  6 02:56:34 IST 2025
