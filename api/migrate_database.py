#!/usr/bin/env python3
"""
Database Migration Script
========================

Adds missing columns to the users table for production deployment.
"""

import asyncio
import logging
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.core.database import create_database_engine, SessionLocal, create_database_engine
from app.core.config import get_settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_users_table():
    """Add missing columns to users table."""
    
    # Create engine and session
    engine = create_database_engine()
    
    # SQL commands to add missing columns
    migration_commands = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS first_name VARCHAR(100);",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_name VARCHAR(100);", 
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS organization VARCHAR(255);",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20);",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_notifications BOOLEAN DEFAULT true;",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS theme_preference VARCHAR(20) DEFAULT 'auto';",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS language VARCHAR(10) DEFAULT 'en';"
    ]
    
    with engine.connect() as connection:
        try:
            for command in migration_commands:
                try:
                    logger.info(f"Executing: {command}")
                    connection.execute(text(command))
                    connection.commit()
                    logger.info("✅ Command executed successfully")
                except OperationalError as e:
                    if "already exists" in str(e).lower():
                        logger.info("ℹ️ Column already exists, skipping")
                    else:
                        logger.error(f"❌ Error executing command: {e}")
                        raise
                except Exception as e:
                    logger.error(f"❌ Unexpected error: {e}")
                    raise
            
            logger.info("✅ Database migration completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            raise


if __name__ == "__main__":
    logger.info("🔄 Starting database migration...")
    migrate_users_table()
    logger.info("🎉 Migration completed!")
