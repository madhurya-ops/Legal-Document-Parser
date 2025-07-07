#!/usr/bin/env python3
"""
Setup script for creating initial admin user and initializing the database.
Run this once after setting up the database.
"""

import os
import sys
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app import models, auth, schemas

def create_admin_user():
    """Create the initial admin user"""
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Admin user credentials
        admin_email = os.getenv("ADMIN_EMAIL", "admin@legaldoc.com")
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "AdminPassword123!")
        
        print(f"Creating admin user...")
        print(f"Email: {admin_email}")
        print(f"Username: {admin_username}")
        
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
        
        # Create some sample system metrics
        from app import crud
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
        print(f"❌ Error creating admin user: {e}")
        sys.exit(1)
    finally:
        db.close()

def main():
    """Main setup function"""
    print("🚀 Setting up LegalDoc Admin User...")
    print("=" * 50)
    
    # Check if required environment variables are set
    if not os.getenv("SECRET_KEY"):
        print("⚠️  Warning: SECRET_KEY not set in environment variables")
        print("Using default key for development only!")
    
    if not os.getenv("DATABASE_URL"):
        print("⚠️  Warning: DATABASE_URL not set in environment variables")
        print("Using default SQLite database for development!")
    
    create_admin_user()
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the backend server: uvicorn app.main:app --reload")
    print("2. Access the admin dashboard at: http://localhost:8000/api/admin/dashboard")
    print("3. API documentation at: http://localhost:8000/docs")
    print("\nDefault admin credentials:")
    print(f"Email: {os.getenv('ADMIN_EMAIL', 'admin@legaldoc.com')}")
    print(f"Password: {os.getenv('ADMIN_PASSWORD', 'AdminPassword123!')}")

if __name__ == "__main__":
    main()
# update Sun Jul  6 02:55:00 IST 2025
# update Sun Jul  6 02:56:34 IST 2025
