#!/usr/bin/env python3
"""
Integration Verification Script
==============================

This script verifies that the frontend and backend are properly integrated
and all major components are working correctly.
"""

import os
import sys
import requests
import time
import json
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def check_service(url, name, timeout=5):
    """Check if a service is running and responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name} is running at {url}")
            return True
        else:
            print(f"❌ {name} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {name} is not accessible: {e}")
        return False

def check_api_endpoints():
    """Test critical API endpoints"""
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/docs", "API documentation"),
    ]
    
    print("\n🔍 Testing API endpoints...")
    
    all_good = True
    for endpoint, description in endpoints:
        url = f"{BACKEND_URL}{endpoint}"
        if check_service(url, description):
            continue
        else:
            all_good = False
    
    return all_good

def check_frontend_files():
    """Check if frontend files exist"""
    print("\n📁 Checking frontend file structure...")
    
    frontend_files = [
        "web/my-app/package.json",
        "web/my-app/src/App.js",
        "web/my-app/src/api.js",
        "web/my-app/src/components/AdminDashboard.js",
        "web/my-app/src/components/FileUpload.js",
        "web/my-app/src/components/ChatInterface.js",
    ]
    
    all_exist = True
    for file_path in frontend_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def check_backend_files():
    """Check if backend files exist"""
    print("\n📁 Checking backend file structure...")
    
    backend_files = [
        "api/app/main.py",
        "api/app/api/__init__.py",
        "api/app/api/admin.py",
        "api/app/api/auth.py",
        "api/app/api/documents.py",
        "api/app/api/legal.py",
        "api/app/api/query.py",
        "api/app/services/llm_client.py",
        "api/app/services/vector_store.py",
        "api/app/services/legal_analysis.py",
        "api/requirements.txt",
    ]
    
    all_exist = True
    for file_path in backend_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def check_environment_files():
    """Check environment configuration"""
    print("\n⚙️  Checking environment configuration...")
    
    env_files = [
        ("api/.env.example", "Backend env example"),
        ("config/production.env", "Production config"),
        ("start_dev.py", "Development script"),
        ("deploy/docker-compose.yml", "Docker compose"),
    ]
    
    all_exist = True
    for file_path, description in env_files:
        if Path(file_path).exists():
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} missing")
            all_exist = False
    
    return all_exist

def test_api_integration():
    """Test API integration points"""
    print("\n🔗 Testing API integration...")
    
    try:
        # Test root endpoint
        response = requests.get(f"{BACKEND_URL}/")
        if response.status_code == 200:
            data = response.json()
            if "LegalDoc API" in data.get("message", ""):
                print("✅ Backend API root endpoint working")
            else:
                print("❌ Backend API root endpoint returned unexpected data")
                return False
        else:
            print("❌ Backend API root endpoint not accessible")
            return False
            
        # Test health endpoint
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✅ Backend health check working")
            else:
                print("❌ Backend health check returned unexpected status")
                return False
        else:
            print("❌ Backend health endpoint not accessible")
            return False
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API integration test failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 Legal Document Parser - Integration Verification")
    print("=" * 55)
    
    all_checks_passed = True
    
    # Check if services are running
    print("\n🌐 Checking running services...")
    backend_running = check_service(BACKEND_URL, "Backend API")
    frontend_running = check_service(FRONTEND_URL, "Frontend", timeout=2)
    
    if not backend_running:
        print("\n⚠️  Backend is not running. Start it with:")
        print("   cd api && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        all_checks_passed = False
    
    if not frontend_running:
        print("\n⚠️  Frontend is not running. Start it with:")
        print("   cd web/my-app && npm start")
        all_checks_passed = False
    
    # File structure checks
    if not check_backend_files():
        all_checks_passed = False
    
    if not check_frontend_files():
        all_checks_passed = False
    
    if not check_environment_files():
        all_checks_passed = False
    
    # API integration tests
    if backend_running:
        if not check_api_endpoints():
            all_checks_passed = False
        
        if not test_api_integration():
            all_checks_passed = False
    
    # Final summary
    print("\n" + "=" * 55)
    if all_checks_passed:
        print("🎉 All integration checks passed!")
        print("\n✨ Your Legal Document Parser is ready to use!")
        print(f"   Frontend: {FRONTEND_URL}")
        print(f"   Backend:  {BACKEND_URL}")
        print(f"   API Docs: {BACKEND_URL}/docs")
    else:
        print("❌ Some integration checks failed.")
        print("\n🔧 Please fix the issues above and run this script again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
