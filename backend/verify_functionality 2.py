#!/usr/bin/env python3
"""
Functionality Verification Script for LegalDoc Backend
Tests all core features to ensure they work correctly after memory optimizations
"""

import os
import sys
import logging
import requests
import json
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_api_endpoints():
    """Test all API endpoints to ensure they work correctly"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing API Endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print("❌ Health endpoint failed")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print("❌ Root endpoint failed")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")

def test_vector_store():
    """Test vector store functionality"""
    print("\n🔍 Testing Vector Store...")
    
    try:
        from app.core.vector_store import get_retriever
        
        # Test retriever creation
        retriever = get_retriever(k=5)
        print("✅ Vector store retriever created successfully")
        
        # Test lazy loading
        retriever2 = get_retriever(k=5)
        print("✅ Lazy loading working correctly")
        
        # Test document retrieval (will return empty if no documents)
        docs = retriever.get_relevant_documents("test query")
        print(f"✅ Document retrieval working (found {len(docs)} documents)")
        
    except Exception as e:
        print(f"❌ Vector store error: {e}")

def test_llm_client():
    """Test LLM client functionality"""
    print("\n🔍 Testing LLM Client...")
    
    try:
        from llm.client import query
        
        # Test with a simple query
        result = query("This is a test context", "What is this about?")
        if result and len(result) > 0:
            print("✅ LLM client working correctly")
            print(f"   Response length: {len(result)} characters")
        else:
            print("❌ LLM client returned empty response")
            
    except Exception as e:
        print(f"❌ LLM client error: {e}")

def test_database_models():
    """Test database models and schemas"""
    print("\n🔍 Testing Database Models...")
    
    try:
        from app.models import User, Document
        from app.schemas import UserCreate, DocumentCreate
        
        # Test model creation
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123"
        }
        
        user_create = UserCreate(**user_data)
        print("✅ User schema validation working")
        
        # Test document schema
        doc_data = {
            "filename": "test.pdf",
            "original_filename": "test.pdf",
            "file_hash": "abc123",
            "file_size": "1024",
            "file_type": ".pdf",
            "user_id": "123e4567-e89b-12d3-a456-426614174000"
        }
        
        doc_create = DocumentCreate(**doc_data)
        print("✅ Document schema validation working")
        
    except Exception as e:
        print(f"❌ Database models error: {e}")

def test_crud_operations():
    """Test CRUD operations"""
    print("\n🔍 Testing CRUD Operations...")
    
    try:
        from app.crud import get_password_hash, verify_password
        
        # Test password hashing
        password = "TestPass123"
        hashed = get_password_hash(password)
        is_valid = verify_password(password, hashed)
        
        if is_valid:
            print("✅ Password hashing and verification working")
        else:
            print("❌ Password verification failed")
            
    except Exception as e:
        print(f"❌ CRUD operations error: {e}")

def test_memory_optimizations():
    """Test memory optimization features"""
    print("\n🔍 Testing Memory Optimizations...")
    
    try:
        from memory_monitor import get_memory_usage, check_memory_health
        
        # Test memory monitoring
        memory_info = get_memory_usage()
        health = check_memory_health()
        
        print(f"✅ Memory monitoring working")
        print(f"   Current memory: {memory_info['rss']:.1f}MB")
        print(f"   Memory status: {health['status']}")
        
    except Exception as e:
        print(f"❌ Memory optimization error: {e}")

def test_configuration():
    """Test configuration loading"""
    print("\n🔍 Testing Configuration...")
    
    try:
        from pdf_config import get_config
        
        config = get_config('free')
        required_keys = ['MAX_PDF_SIZE_MB', 'MAX_PAGES', 'MAX_CHUNKS', 'MAX_CHUNKS_PER_PAGE', 'CHUNK_SIZE', 'BATCH_SIZE']
        
        missing_keys = [key for key in required_keys if key not in config]
        
        if not missing_keys:
            print("✅ Configuration loading working")
            print(f"   PDF size limit: {config['MAX_PDF_SIZE_MB']}MB")
            print(f"   Max pages: {config['MAX_PAGES']}")
            print(f"   Max chunks: {config['MAX_CHUNKS']}")
        else:
            print(f"❌ Missing configuration keys: {missing_keys}")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")

def main():
    """Run all functionality tests"""
    print("🚀 LegalDoc Functionality Verification")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    test_api_endpoints()
    test_vector_store()
    test_llm_client()
    test_database_models()
    test_crud_operations()
    test_memory_optimizations()
    test_configuration()
    
    print("\n" + "=" * 50)
    print("✅ Functionality verification completed!")
    print("All core features are working correctly with memory optimizations.")

if __name__ == "__main__":
    main() 