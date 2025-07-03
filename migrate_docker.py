import os
import sys
from sqlalchemy import text
from app.database import SessionLocal, engine
from app import models

def migrate_database():
    print("🔄 Starting database migration...")
    
    # Drop and recreate all tables with new schema
    print("📋 Dropping and recreating tables...")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    print("✅ Database migration completed!")
    print("📝 Tables created:")
    
    # List all tables
    for table in models.Base.metadata.tables.keys():
        print(f"  - {table}")

def create_admin():
    """Create admin user after migration"""
    from app import auth, schemas, crud
    
    db = SessionLocal()
    try:
        # Admin user credentials
        admin_email = "admin@legaldoc.com"
        admin_username = "admin"
        admin_password = "AdminPassword123!"
        
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
        print(f"❌ Error creating admin: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 LegalDoc Database Migration and Setup...")
    print("=" * 50)
    
    try:
        # Step 1: Migrate database
        migrate_database()
        
        # Step 2: Create admin user
        create_admin()
        
        print("=" * 50)
        print("🎉 Migration and setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
