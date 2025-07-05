from app.database import SessionLocal
from app import models
from sqlalchemy import text

def fix_admin_role():
    db = SessionLocal()
    try:
        # Find the admin user
        admin_user = db.query(models.User).filter(models.User.email == "admin@legaldoc.com").first()
        
        if admin_user:
            print(f"Found admin user: {admin_user.username}")
            print(f"Current role: {admin_user.role}")
            
            # Update role using raw SQL to handle enum properly
            db.execute(
                text("UPDATE users SET role = 'admin' WHERE email = :email"),
                {"email": "admin@legaldoc.com"}
            )
            db.commit()
            
            # Refresh and check
            db.refresh(admin_user)
            print(f"Updated role: {admin_user.role}")
            print("✅ Admin role updated successfully!")
        else:
            print("❌ Admin user not found")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_admin_role()
# update Sun Jul  6 02:56:34 IST 2025
