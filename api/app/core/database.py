"""
Database Configuration
======================

Production-ready database setup with connection pooling and async support.
"""

import logging
from typing import AsyncGenerator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from .config import get_settings

logger = logging.getLogger(__name__)

# Create the base class for models
Base = declarative_base()
metadata = MetaData()

# Global engine and session variables
engine = None
async_engine = None
SessionLocal = None
AsyncSessionLocal = None


def get_database_url(async_driver: bool = False) -> str:
    """Get database URL with appropriate driver."""
    settings = get_settings()
    url = settings.database_url
    
    if async_driver:
        # Convert to async URL
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("sqlite:///"):
            url = url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    
    return url


def create_database_engine():
    """Create synchronous database engine."""
    global engine, SessionLocal
    
    if engine is not None:
        return engine
    
    database_url = get_database_url(async_driver=False)
    
    # Engine configuration for production
    engine_kwargs = {
        "poolclass": QueuePool,
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "echo": get_settings().debug
    }
    
    # SQLite specific configuration
    if database_url.startswith("sqlite"):
        engine_kwargs.update({
            "poolclass": None,
            "connect_args": {"check_same_thread": False}
        })
    
    engine = create_engine(database_url, **engine_kwargs)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    logger.info(f"✅ Database engine created: {database_url}")
    return engine


def create_async_database_engine():
    """Create asynchronous database engine."""
    global async_engine, AsyncSessionLocal
    
    if async_engine is not None:
        return async_engine
    
    database_url = get_database_url(async_driver=True)
    
    # Async engine configuration
    engine_kwargs = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "echo": get_settings().debug
    }
    
    async_engine = create_async_engine(database_url, **engine_kwargs)
    AsyncSessionLocal = async_sessionmaker(
        async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    logger.info(f"✅ Async database engine created: {database_url}")
    return async_engine


def get_db() -> Session:
    """Dependency to get synchronous database session."""
    if SessionLocal is None:
        create_database_engine()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get asynchronous database session."""
    if AsyncSessionLocal is None:
        create_async_database_engine()
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    from app.models import user, document, chat, analysis
    
    # Create sync engine for table creation
    sync_engine = create_database_engine()
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=sync_engine)
        logger.info("✅ Database tables created successfully")
        
        # Create initial admin user if it doesn't exist
        await create_initial_admin()
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise


async def create_initial_admin():
    """Create initial admin user if it doesn't exist."""
    from app.models.user import User, UserRole
    from app.core.security import get_password_hash
    
    settings = get_settings()
    
    try:
        # Use sync session for initial setup
        if SessionLocal is None:
            create_database_engine()
        
        db = SessionLocal()
        try:
            # Check if admin user exists
            existing_admin = db.query(User).filter(
                User.email == settings.initial_admin_email
            ).first()
            
            if not existing_admin:
                # Create admin user directly
                hashed_password = get_password_hash(settings.initial_admin_password)
                admin_user = User(
                    username=settings.initial_admin_username,
                    email=settings.initial_admin_email,
                    hashed_password=hashed_password,
                    role=UserRole.ADMIN,
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                db.refresh(admin_user)
                logger.info(f"✅ Initial admin user created: {admin_user.email}")
            else:
                logger.info("ℹ️ Admin user already exists")
        
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"❌ Failed to create initial admin: {e}")


def close_db_connections():
    """Close database connections."""
    global engine, async_engine
    
    if engine:
        engine.dispose()
        logger.info("✅ Sync database connections closed")
    
    if async_engine:
        async_engine.dispose()
        logger.info("✅ Async database connections closed")
