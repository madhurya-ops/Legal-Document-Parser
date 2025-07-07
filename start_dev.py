#!/usr/bin/env python3
"""
Development startup script for LegalDoc API
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def setup_environment():
    """Setup development environment"""
    print("🔧 Setting up development environment...")
    
    # Check if .env exists
    env_file = Path("api/.env")
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        with open("api/.env.example") as template:
            content = template.read()
        with open(env_file, "w") as env:
            env.write(content)
        print("⚠️  Please update api/.env with your actual configuration")
    
    # Install dependencies
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "api/requirements.txt"
        ], check=True, cwd=".")
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def start_api_server(host="0.0.0.0", port=8000, reload=True):
    """Start the FastAPI development server"""
    print(f"🚀 Starting LegalDoc API server on {host}:{port}")
    print(f"📖 API Documentation: http://localhost:{port}/docs")
    print(f"🔗 API Base URL: http://localhost:{port}")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app",
            "--host", host,
            "--port", str(port),
            "--reload" if reload else "--no-reload"
        ], cwd="api")
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="LegalDoc Development Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    parser.add_argument("--setup-only", action="store_true", help="Setup environment only")
    
    args = parser.parse_args()
    
    print("🏁 LegalDoc Development Setup")
    print("=" * 40)
    
    check_python_version()
    setup_environment()
    
    if args.setup_only:
        print("✅ Environment setup complete")
        return
    
    start_api_server(
        host=args.host,
        port=args.port,
        reload=not args.no_reload
    )

if __name__ == "__main__":
    main()
