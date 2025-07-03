from app.database import SessionLocal
from app import models

def check_users():
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        print("📋 Users in database:")
        for user in users:
            print(f"  - ID: {user.id}")
            print(f"    Username: {user.username}")
            print(f"    Email: {user.email}")
            print(f"    Role: {user.role} (type: {type(user.role)})")
            print(f"    Active: {user.is_active}")
            print("    ---")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
