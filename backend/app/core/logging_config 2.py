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
# setup_logging() 