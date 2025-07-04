import os
import sys
from app.database import SessionLocal
from app import models, schemas, crud

def create_admin():
    """Create admin user with correct enum handling"""
    db = SessionLocal()
    try:
        # Admin user credentials
        admin_email = "admin@legaldoc.com"
        admin_username = "admin"
        admin_password = "AdminPassword123!"
        
        print(f"👤 Creating admin user...")
        print(f"Email: {admin_email}")
        print(f"Username: {admin_username}")
        
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == admin_email).first()
        if existing_user:
            print("Admin user already exists!")
            return
        
        # Hash the password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(admin_password)
        
        # Create admin user directly
        admin_user = models.User(
            username=admin_username,
            email=admin_email,
            hashed_password=hashed_password,
            role=models.UserRole.ADMIN,  # Set admin role directly
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
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
            metric = models.SystemMetric(
                metric_name=metric_data["metric_name"],
                metric_value=metric_data["metric_value"]
            )
            db.add(metric)
        
        db.commit()
        
        print("✅ Sample system metrics created!")
        
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Creating LegalDoc Admin User...")
    print("=" * 40)
    
    create_admin()
    
    print("=" * 40)
    print("🎉 Admin user setup completed successfully!")
    print("\n🔑 Admin credentials:")
    print("• Email: admin@legaldoc.com")
    print("• Password: AdminPassword123!")
