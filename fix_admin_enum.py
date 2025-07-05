from app.database import SessionLocal
from app import models
from sqlalchemy import text

def fix_admin_role():
    db = SessionLocal()
    try:
        # Check what enum values exist
        result = db.execute(text("SELECT unnest(enum_range(NULL::userrole))"))
        enum_values = [row[0] for row in result]
        print(f"Available enum values: {enum_values}")
        
        # Find the admin user
        admin_user = db.query(models.User).filter(models.User.email == "admin@legaldoc.com").first()
        
        if admin_user:
            print(f"Found admin user: {admin_user.username}")
            print(f"Current role: {admin_user.role}")
            
            # Try different enum values
            for enum_val in ['ADMIN', 'admin', 'Admin']:
                if enum_val in enum_values:
                    print(f"Using enum value: {enum_val}")
                    db.execute(
                        text(f"UPDATE users SET role = '{enum_val}' WHERE email = :email"),
                        {"email": "admin@legaldoc.com"}
                    )
                    db.commit()
                    
                    # Refresh and check
                    db.refresh(admin_user)
                    print(f"Updated role: {admin_user.role}")
                    print("✅ Admin role updated successfully!")
                    return
            
            print("❌ Could not find matching enum value")
        else:
            print("❌ Admin user not found")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_admin_role()
# update Sun Jul  6 02:56:34 IST 2025
