"""
User Model
==========

User data model with authentication and role management.
"""

import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..core.database import Base


class UserRole(enum.Enum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"


class User(Base):
    """User model for authentication and user management."""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication fields
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Made nullable for Auth0 users
    
    # Auth0 integration
    auth0_sub = Column(String(255), unique=True, index=True, nullable=True)
    
    # User status
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Profile information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    organization = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Preferences
    email_notifications = Column(Boolean, default=True)
    theme_preference = Column(String(20), default="auto")  # light, dark, auto
    language = Column(String(10), default="en")
    
    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        """String representation of user."""
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN
    
    def to_dict(self) -> dict:
        """Convert user to dictionary (excluding sensitive data)."""
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "role": self.role.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "organization": self.organization,
            "phone": self.phone,
            "email_notifications": self.email_notifications,
            "theme_preference": self.theme_preference,
            "language": self.language,
            "is_admin": self.is_admin
        }
