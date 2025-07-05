from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from . import crud, schemas
from .database import get_db
from .models import UserRole

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception: HTTPException) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject: Optional[str] = payload.get("sub")
        if subject is None:
            raise credentials_exception
        return subject
    except JWTError:
        raise credentials_exception

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    email = verify_access_token(token, credentials_exception)
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(
    current_user: schemas.UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Update last login timestamp
    crud.update_user_last_login(db, str(current_user.id))
    
    return current_user

def require_admin(
    current_user: schemas.UserResponse = Depends(get_current_active_user)
):
    """Dependency to require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def create_admin_user(db: Session, email: str, username: str, password: str) -> schemas.UserResponse:
    """Create an admin user - for initial setup only"""
    # Check if user already exists
    existing_user = crud.get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create user with admin role
    user_data = schemas.UserCreate(
        email=email,
        username=username,
        password=password
    )
    
    user = crud.create_user(db, user_data)
    
    # Update role to admin
    update_data = schemas.UserUpdate(role=UserRole.ADMIN)
    admin_user = crud.update_user(db, str(user.id), update_data)
    
    return schemas.UserResponse.from_orm(admin_user)
# update Sun Jul  6 02:54:59 IST 2025
