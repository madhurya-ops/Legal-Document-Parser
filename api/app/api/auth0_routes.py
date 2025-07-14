"""
Auth0 Authentication Routes
===========================

Modern OAuth 2.0 + OpenID Connect authentication routes using Auth0.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import httpx
import json

from ..core.auth0 import (
    get_auth0_user,
    get_current_user_from_auth0,
    require_admin_auth0,
    get_token_info
)
from ..core.database import get_db
from ..core.config import get_settings
from ..schemas import UserResponse
from ..services.crud import update_user_last_login, get_user_by_auth0_sub, create_user_from_auth0

router = APIRouter(prefix="/auth", tags=["Auth0 Authentication"])


@router.get("/protected", response_model=Dict[str, Any])
async def protected_route(
    token_info: Dict[str, Any] = Depends(get_token_info)
) -> Dict[str, Any]:
    """
    Protected route that requires a valid Auth0 access token.
    Returns decoded user info from the token claims.
    """
    return {
        "message": "Access granted to protected resource",
        "user_info": token_info,
        "timestamp": "2025-07-08T10:33:36Z"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user = Depends(get_current_user_from_auth0),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Get current authenticated user information.
    Creates user record if first time Auth0 login.
    """
    # Update last login
    await update_user_last_login(db, str(current_user.id))
    
    return current_user


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user = Depends(get_current_user_from_auth0)
) -> UserResponse:
    """Get user profile information."""
    return current_user


@router.post("/sync")
async def sync_auth0_user(
    auth0_user: Dict[str, Any] = Depends(get_auth0_user),
    current_user = Depends(get_current_user_from_auth0),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Sync user information from Auth0 token.
    Useful for updating user data when Auth0 profile changes.
    """
    # Extract updated info from token
    email = auth0_user.get("email") or auth0_user.get("https://legaldoc.com/email")
    name = auth0_user.get("name") or auth0_user.get("https://legaldoc.com/name")
    
    # Update user if needed
    updated = False
    if email and email != current_user.email:
        current_user.email = email
        updated = True
    
    if name and name != current_user.username:
        # Only update username if it's available
        existing_user = db.query(type(current_user)).filter(
            type(current_user).username == name,
            type(current_user).id != current_user.id
        ).first()
        
        if not existing_user:
            current_user.username = name
            updated = True
    
    if updated:
        db.commit()
        db.refresh(current_user)
    
    return {
        "message": "User profile synced successfully",
        "updated": updated,
        "user": {
            "id": str(current_user.id),
            "username": current_user.username,
            "email": current_user.email,
            "auth0_sub": current_user.auth0_sub
        }
    }


@router.get("/admin/verify")
async def verify_admin_access(
    admin_user = Depends(require_admin_auth0)
) -> Dict[str, Any]:
    """Verify admin access with Auth0 authentication."""
    return {
        "message": "Admin access verified",
        "admin_user": {
            "id": str(admin_user.id),
            "username": admin_user.username,
            "email": admin_user.email,
            "role": admin_user.role.value
        }
    }


@router.get("/token/info")
async def get_token_debug_info(
    token_info: Dict[str, Any] = Depends(get_token_info)
) -> Dict[str, Any]:
    """
    Debug endpoint to inspect token information.
    Useful for development and troubleshooting.
    """
    return {
        "message": "Token information retrieved successfully",
        "token_claims": token_info
    }


@router.get("/health")
async def auth_health_check() -> Dict[str, Any]:
    """Health check for Auth0 authentication system."""
    return {
        "status": "healthy",
        "auth_system": "Auth0",
        "message": "Auth0 authentication system is operational"
    }
