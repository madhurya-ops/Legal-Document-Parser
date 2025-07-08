from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Any

from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.services.crud import get_user_by_email, get_user_by_username, create_user, authenticate_user, update_user_last_login
from app.core.database import get_db
from app.core.security import create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, db: Session = Depends(get_db)) -> Any:
    """Register a new user"""
    existing_user = await get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    existing_username = await get_user_by_username(db, username=user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    return await create_user(db=db, user=user)

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)) -> Any:
    """Authenticate user and return access token"""
    user = await authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Update last login
    await update_user_last_login(db, str(user.id))
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_active_user)) -> Any:
    """Get current user information"""
    return current_user

@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: UserResponse = Depends(get_current_active_user)) -> Any:
    """Refresh access token"""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
