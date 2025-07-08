"""
Security Utilities
==================

Production-ready security utilities for authentication and authorization.
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Union

from passlib.context import CryptContext

from .config import get_settings
from .database import get_db

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class SecurityError(Exception):
    """Base security exception."""
    pass


class AuthenticationError(SecurityError):
    """Authentication related errors."""
    pass


class AuthorizationError(SecurityError):
    """Authorization related errors."""
    pass


def generate_password_hash(password: str) -> str:
    """Generate a secure password hash."""
    return pwd_context.hash(password)


# Alias for compatibility
get_password_hash = generate_password_hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)


def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    settings = get_settings()
    
    raise NotImplementedError("JWT generation is no longer supported. Migrate to Auth0.")








def check_permissions(
    user, 
    resource: str, 
    action: str
) -> bool:
    """Check if user has permission for resource action."""
    from ..models.user import UserRole
    
    # Admin can do everything
    if user.role == UserRole.ADMIN:
        return True
    
    # Resource-specific permissions
    if resource == "document":
        # Users can manage their own documents
        return action in ["read", "create", "update", "delete"]
    
    elif resource == "chat":
        # Users can manage their own chats
        return action in ["read", "create", "update", "delete"]
    
    elif resource == "admin":
        # Only admins can access admin resources
        return False
    
    return False


def hash_file_content(content: bytes) -> str:
    """Generate a secure hash of file content."""
    import hashlib
    return hashlib.sha256(content).hexdigest()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal."""
    import os
    import re
    
    # Remove path components
    filename = os.path.basename(filename)
    
    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename


def validate_file_type(filename: str, allowed_types: list) -> bool:
    """Validate file type against allowed types."""
    import os
    
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in allowed_types


def rate_limit_key(identifier: str, action: str) -> str:
    """Generate rate limit key."""
    return f"rate_limit:{action}:{identifier}"
