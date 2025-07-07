"""
Security Utilities
==================

Production-ready security utilities for authentication and authorization.
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token security
security = HTTPBearer()

# Token expiration constant for backward compatibility
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours


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
    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def verify_access_token(token: str) -> dict:
    """Verify and decode a JWT access token."""
    settings = get_settings()
    
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        
        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            raise AuthenticationError("Token has expired")
        
        return payload
        
    except JWTError as e:
        raise AuthenticationError(f"Invalid token: {str(e)}")


def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user from JWT token."""
    from ..models.user import User
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify token
        payload = verify_access_token(credentials.credentials)
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except AuthenticationError:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def get_current_active_user(
    current_user = Depends(get_current_user_from_token)
):
    """Get current active user."""
    return current_user


def require_admin(
    current_user = Depends(get_current_active_user)
):
    """Require admin role."""
    from ..models.user import UserRole
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


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
