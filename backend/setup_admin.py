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
    """Create the initial admin users (4 admins)"""
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Admin users to create - 4 admins as requested
        admin_users = [
            {
                "username": "admin1",
                "email": "admin1@legaldoc.com",
                "password": "AdminPass123!",
                "role": "admin"
            },
            {
                "username": "admin2", 
                "email": "admin2@legaldoc.com",
                "password": "AdminPass456!",
                "role": "admin"
            },
            {
                "username": "admin3",
                "email": "admin3@legaldoc.com",
                "password": "AdminPass789!",
                "role": "admin"
            },
            {
                "username": "admin4",
                "email": "admin4@legaldoc.com",
                "password": "AdminPass101!",
                "role": "admin"
            }
        ]
        
        print(f"Creating {len(admin_users)} admin users...")
        
        created_admins = []
        for admin_data in admin_users:
            try:
                # Check if admin already exists
                existing_user = db.query(models.User).filter(
                    (models.User.email == admin_data["email"]) | 
                    (models.User.username == admin_data["username"])
                ).first()
                
                if existing_user:
                    print(f"⚠️  Admin {admin_data['username']} already exists, skipping...")
                    continue
                
                print(f"Creating admin: {admin_data['username']} ({admin_data['email']})")
                
                # Create admin user
                admin_user = auth.create_admin_user(
                    db=db,
                    email=admin_data["email"],
                    username=admin_data["username"],
                    password=admin_data["password"]
                )
                
                created_admins.append(admin_user)
                print(f"✅ Admin {admin_data['username']} created successfully!")
                
            except Exception as e:
                print(f"❌ Error creating admin {admin_data['username']}: {e}")
                continue
        
        print(f"\n✅ Successfully created {len(created_admins)} admin users!")
        for admin in created_admins:
            print(f"  - {admin.username} (ID: {admin.id}, Role: {admin.role})")
        
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
