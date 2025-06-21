#!/usr/bin/env python3
"""
Database initialization script
Run this to set up the database tables
"""

import os
import sys
from sqlalchemy import text
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models import Base

def init_database():
    """Initialize the database with tables"""
    print("🗄️  Initializing database...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Test database connection
        with SessionLocal() as db:
            result = db.execute(text("SELECT version();"))
            row = result.fetchone()
            if row:
                version = row[0]
                print(f"✅ Database connection successful! PostgreSQL version: {version}")
            else:
                print("✅ Database connection successful!")
            
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def check_database_connection():
    """Check if database is accessible"""
    print("🔍 Checking database connection...")
    
    try:
        with SessionLocal() as db:
            result = db.execute(text("SELECT 1;"))
            result.fetchone()
            print("✅ Database connection is working!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Make sure PostgreSQL is running and accessible.")
        return False

def main():
    """Main function"""
    load_dotenv()
    
    print("🚀 Database Setup")
    print("=" * 40)
    
    # Check connection first
    if not check_database_connection():
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your DATABASE_URL environment variable")
        print("3. If using Docker, make sure the db service is up")
        return
    
    # Initialize database
    if init_database():
        print("\n🎉 Database setup completed successfully!")
        print("You can now start the FastAPI application.")
    else:
        print("\n❌ Database setup failed!")

if __name__ == "__main__":
    main() 