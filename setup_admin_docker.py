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
            if existing_user.role.value == "admin":
                print("User already has admin role!")
            else:
                # Update existing user to admin
                update_data = schemas.UserUpdate(role=schemas.UserRole.ADMIN)
                admin_user = crud.update_user(db, str(existing_user.id), update_data)
                print(f"✅ Updated existing user to admin role!")
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
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
