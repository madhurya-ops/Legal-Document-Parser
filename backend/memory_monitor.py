#!/usr/bin/env python3
"""
Memory Monitor for LegalDoc Backend
Monitors memory usage and provides optimization suggestions
"""

import psutil
import os
import gc
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return {
        'rss': memory_info.rss / 1024 / 1024,  # Resident Set Size in MB
        'vms': memory_info.vms / 1024 / 1024,  # Virtual Memory Size in MB
        'percent': process.memory_percent()
    }

def get_system_memory():
    """Get system memory information"""
    memory = psutil.virtual_memory()
    return {
        'total': memory.total / 1024 / 1024,  # Total RAM in MB
        'available': memory.available / 1024 / 1024,  # Available RAM in MB
        'used': memory.used / 1024 / 1024,  # Used RAM in MB
        'percent': memory.percent
    }

def check_memory_health():
    """Check if memory usage is healthy"""
    process_memory = get_memory_usage()
    system_memory = get_system_memory()
    
    # Memory thresholds
    CRITICAL_THRESHOLD = 450  # MB
    WARNING_THRESHOLD = 350   # MB
    
    status = "HEALTHY"
    if process_memory['rss'] > CRITICAL_THRESHOLD:
        status = "CRITICAL"
    elif process_memory['rss'] > WARNING_THRESHOLD:
        status = "WARNING"
    
    return {
        'status': status,
        'process_memory': process_memory,
        'system_memory': system_memory,
        'timestamp': datetime.now().isoformat()
    }

def optimize_memory():
    """Perform memory optimization"""
    logging.info("Performing memory optimization...")
    
    # Force garbage collection
    collected = gc.collect()
    logging.info(f"Garbage collection freed {collected} objects")
    
    # Get memory usage after optimization
    memory_info = get_memory_usage()
    logging.info(f"Memory usage after optimization: {memory_info['rss']:.1f}MB")
    
    return memory_info

def log_memory_usage():
    """Log current memory usage"""
    health = check_memory_health()
    
    logging.info(f"Memory Status: {health['status']}")
    logging.info(f"Process Memory: {health['process_memory']['rss']:.1f}MB RSS, {health['process_memory']['percent']:.1f}%")
    logging.info(f"System Memory: {health['system_memory']['used']:.1f}MB used, {health['system_memory']['percent']:.1f}%")
    
    if health['status'] != "HEALTHY":
        logging.warning(f"Memory usage is {health['status']} - consider optimization")
    
    return health

if __name__ == "__main__":
    print("LegalDoc Memory Monitor")
    print("=" * 30)
    
    # Initial memory check
    health = log_memory_usage()
    
    # Optimization suggestions
    if health['process_memory']['rss'] > 300:
        print("\nOptimization Suggestions:")
        print("- Reduce document processing limits")
        print("- Implement lazy loading for models")
        print("- Clear unused variables")
        print("- Restart application if needed")
    
    # Perform optimization if needed
    if health['status'] == "CRITICAL":
        print("\nPerforming emergency memory optimization...")
        optimize_memory() # update Sun Jul  6 02:55:00 IST 2025
# update Sun Jul  6 02:56:34 IST 2025
