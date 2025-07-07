#!/usr/bin/env python3
"""
Docker setup script for LegalDoc application.
This script will set up the admin user after the Docker containers are running.
"""

import subprocess
import time
import sys
import os

def run_command(command, description):
    """Run a command and handle output"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout.strip():
                print(result.stdout)
        else:
            print(f"❌ {description} failed!")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def wait_for_backend():
    """Wait for the backend to be ready"""
    print("⏳ Waiting for backend to be ready...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            result = subprocess.run(
                "curl -s http://localhost:8000/health", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                print("✅ Backend is ready!")
                return True
        except:
            pass
        
        print(f"⏳ Attempt {attempt + 1}/{max_attempts} - waiting for backend...")
        time.sleep(5)
    
    print("❌ Backend failed to start within expected time")
    return False

def setup_admin_user():
    """Set up the admin user in the Docker container"""
    
    # Create a temporary script for the container
    admin_script = """
import os
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import auth, schemas, crud, models

def create_admin():
    db = SessionLocal()
    try:
        # Admin user credentials
        admin_email = "admin@legaldoc.com"
        admin_username = "admin"
        admin_password = "AdminPassword123!"
        
        print(f"Creating admin user...")
        print(f"Email: {admin_email}")
        print(f"Username: {admin_username}")
        
        # Check if admin already exists
        existing_user = crud.get_user_by_email(db, admin_email)
        if existing_user:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin_user = auth.create_admin_user(
            db=db,
            email=admin_email,
            username=admin_username,
            password=admin_password
        )
        
        print(f"✅ Admin user created successfully!")
        print(f"User ID: {admin_user.id}")
        print(f"Role: {admin_user.role}")
        
        # Create sample metrics
        sample_metrics = [
            {"metric_name": "daily_active_users", "metric_value": {"count": 0, "date": "2024-01-01"}},
            {"metric_name": "api_calls", "metric_value": {"count": 0, "endpoint": "total"}},
            {"metric_name": "document_uploads", "metric_value": {"count": 0, "date": "2024-01-01"}},
        ]
        
        for metric_data in sample_metrics:
            metric = schemas.SystemMetricCreate(**metric_data)
            crud.create_system_metric(db, metric)
        
        print("✅ Sample system metrics created!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
"""
    
    # Write the script to a temporary file
    with open("/tmp/setup_admin_docker.py", "w") as f:
        f.write(admin_script)
    
    # Copy the script to the container and run it
    commands = [
        "docker cp /tmp/setup_admin_docker.py legal-document-parser-backend-1:/app/setup_admin_docker.py",
        "docker exec legal-document-parser-backend-1 python setup_admin_docker.py"
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Running: {cmd}"):
            return False
    
    # Clean up
    os.remove("/tmp/setup_admin_docker.py")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up LegalDoc with Docker...")
    print("=" * 60)
    
    # Step 1: Start Docker containers
    if not run_command("docker-compose up --build -d", "Starting Docker containers"):
        sys.exit(1)
    
    # Step 2: Wait for backend to be ready
    if not wait_for_backend():
        print("❌ Backend failed to start. Check logs with: docker-compose logs backend")
        sys.exit(1)
    
    # Step 3: Set up admin user
    print("\n👤 Setting up admin user...")
    if not setup_admin_user():
        print("❌ Failed to set up admin user")
        sys.exit(1)
    
    print("=" * 60)
    print("🎉 LegalDoc setup completed successfully!")
    print("\n📋 Service URLs:")
    print("• Frontend: http://localhost:3000")
    print("• Backend API: http://localhost:8000")
    print("• API Documentation: http://localhost:8000/docs")
    print("• Admin Dashboard: http://localhost:8000/api/admin/dashboard")
    
    print("\n🔑 Default admin credentials:")
    print("• Email: admin@legaldoc.com")
    print("• Password: AdminPassword123!")
    
    print("\n🔧 Useful commands:")
    print("• View logs: docker-compose logs -f")
    print("• Stop services: docker-compose down")
    print("• Restart services: docker-compose restart")
    print("• Access backend shell: docker exec -it legal-document-parser-backend-1 bash")

if __name__ == "__main__":
    main()
# update Sun Jul  6 02:56:34 IST 2025
