#!/usr/bin/env python3
"""
Database migration script to handle schema updates for development.
This script will create a new SQLite database with the updated schema.
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models

def migrate_database():
    """Create or recreate database with new schema"""
    
    # Use SQLite for development if PostgreSQL is not available
    database_url = "sqlite:///./legaldoc_dev.db"
    
    print("🔄 Setting up database with new schema...")
    print(f"Database: {database_url}")
    
    # Create engine
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    
    # Create all tables with new schema
    print("📋 Creating database tables...")
    models.Base.metadata.drop_all(bind=engine)  # Drop existing tables
    models.Base.metadata.create_all(bind=engine)  # Create new tables
    
    print("✅ Database migration completed!")
    print("📝 New tables created:")
    
    # List all tables
    for table in models.Base.metadata.tables.keys():
        print(f"  - {table}")
    
    return engine

def create_admin_user_sqlite():
    """Create admin user with SQLite database"""
    
    # Import after setting up the database
    from app import auth, schemas, crud
    from sqlalchemy.orm import Session
    
    # Create engine and session
    engine = migrate_database()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        # Admin user credentials
        admin_email = os.getenv("ADMIN_EMAIL", "admin@legaldoc.com")
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "AdminPassword123!")
        
        print(f"\n👤 Creating admin user...")
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
        sample_metrics = [
            {"metric_name": "daily_active_users", "metric_value": {"count": 0, "date": "2024-01-01"}},
            {"metric_name": "api_calls", "metric_value": {"count": 0, "endpoint": "total"}},
            {"metric_name": "document_uploads", "metric_value": {"count": 0, "date": "2024-01-01"}},
        ]
        
        for metric_data in sample_metrics:
            metric = schemas.SystemMetricCreate(**metric_data)
            crud.create_system_metric(db, metric)
        
        print("✅ Sample system metrics created!")
        
        # Update the database URL in environment for the application
        print(f"\n🔧 To use this database, set the following environment variable:")
        print(f"export DATABASE_URL=sqlite:///./legaldoc_dev.db")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        sys.exit(1)
    finally:
        db.close()

def main():
    """Main migration function"""
    print("🚀 LegalDoc Database Migration...")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "migrate-only":
        # Just migrate the database
        migrate_database()
    else:
        # Migrate and create admin user
        create_admin_user_sqlite()
    
    print("=" * 50)
    print("🎉 Migration completed successfully!")
    print("\nNext steps:")
    print("1. Set environment variable: export DATABASE_URL=sqlite:///./legaldoc_dev.db")
    print("2. Start the backend server: python3 -m uvicorn app.main:app --reload")
    print("3. Access the API documentation at: http://localhost:8000/docs")
    print("\nDefault admin credentials:")
    print(f"Email: {os.getenv('ADMIN_EMAIL', 'admin@legaldoc.com')}")
    print(f"Password: {os.getenv('ADMIN_PASSWORD', 'AdminPassword123!')}")

if __name__ == "__main__":
    main()
# update Sun Jul  6 02:55:00 IST 2025
# update Sun Jul  6 02:56:34 IST 2025
