#!/usr/bin/env python3
"""
Auth0 Migration Script
=====================

Adds Auth0 support to the existing User table.
"""

import logging
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.core.database import create_database_engine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_auth0_support():
    """Add Auth0 support to users table."""
    
    # Create engine
    engine = create_database_engine()
    
    # SQL commands to add Auth0 support
    migration_commands = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS auth0_sub VARCHAR(255);",
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_auth0_sub ON users(auth0_sub);",
        "ALTER TABLE users ALTER COLUMN hashed_password DROP NOT NULL;",  # Make password nullable for Auth0 users
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
                    if "already exists" in str(e).lower() or "does not exist" in str(e).lower():
                        logger.info("ℹ️ Column/Index already exists or constraint already removed, skipping")
                    else:
                        logger.error(f"❌ Error executing command: {e}")
                        raise
                except Exception as e:
                    logger.error(f"❌ Unexpected error: {e}")
                    raise
            
            logger.info("✅ Auth0 migration completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            raise


if __name__ == "__main__":
    logger.info("🔄 Starting Auth0 migration...")
    migrate_auth0_support()
    logger.info("🎉 Auth0 migration completed!")
