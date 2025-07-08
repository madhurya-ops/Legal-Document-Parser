"""
Auth0 Integration
=================

Secure Auth0 OAuth 2.0 + OpenID Connect integration for FastAPI.
"""

import json
import time
from typing import Optional, Dict, Any
from urllib.request import urlopen
from urllib.error import URLError

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db


class Auth0SecurityError(Exception):
    """Auth0 security related errors."""
    pass


class Auth0TokenValidator:
    """Auth0 token validation class."""
    
    def __init__(self):
        self.settings = get_settings()
        self.jwks_cache = {}
        self.jwks_cache_time = 0
        self.jwks_cache_ttl = 300  # 5 minutes cache TTL
        
    def get_jwks(self) -> Dict[str, Any]:
        """Get JWKS from Auth0 with caching."""
        current_time = time.time()
        
        # Check if cache is still valid
        if (self.jwks_cache and 
            current_time - self.jwks_cache_time < self.jwks_cache_ttl):
            return self.jwks_cache
        
        # Fetch fresh JWKS
        try:
            jwks_url = f"https://{self.settings.auth0_domain}/.well-known/jwks.json"
            with urlopen(jwks_url) as response:
                jwks = json.loads(response.read())
                
            self.jwks_cache = jwks
            self.jwks_cache_time = current_time
            return jwks
            
        except URLError as e:
            raise Auth0SecurityError(f"Failed to fetch JWKS: {str(e)}")
        except json.JSONDecodeError as e:
            raise Auth0SecurityError(f"Invalid JWKS response: {str(e)}")
    
    def get_rsa_key(self, token_header: Dict[str, Any]) -> Dict[str, Any]:
        """Get RSA key for token verification."""
        jwks = self.get_jwks()
        
        # Find matching key
        for key in jwks.get("keys", []):
            if key.get("kid") == token_header.get("kid"):
                return {
                    "kty": key.get("kty"),
                    "kid": key.get("kid"),
                    "use": key.get("use"),
                    "n": key.get("n"),
                    "e": key.get("e")
                }
        
        raise Auth0SecurityError("Unable to find appropriate key")
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode Auth0 JWT token."""
        try:
            # Get token header
            unverified_header = jwt.get_unverified_header(token)
            
            # Verify algorithm
            if unverified_header.get("alg") != "RS256":
                raise Auth0SecurityError("Invalid token algorithm")
            
            # Get RSA key
            rsa_key = self.get_rsa_key(unverified_header)
            
            # Verify and decode token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=self.settings.auth0_audience,
                issuer=f"https://{self.settings.auth0_domain}/"
            )
            
            # Additional validation
            self._validate_token_claims(payload)
            
            return payload
            
        except JWTError as e:
            raise Auth0SecurityError(f"Token validation failed: {str(e)}")
        except Exception as e:
            raise Auth0SecurityError(f"Unexpected error during token validation: {str(e)}")
    
    def _validate_token_claims(self, payload: Dict[str, Any]) -> None:
        """Validate additional token claims."""
        # Check required claims
        required_claims = ["sub", "aud", "iss", "exp", "iat"]
        missing_claims = [claim for claim in required_claims if claim not in payload]
        
        if missing_claims:
            raise Auth0SecurityError(f"Missing required claims: {missing_claims}")
        
        # Validate audience
        if payload.get("aud") != self.settings.auth0_audience:
            raise Auth0SecurityError("Invalid audience")
        
        # Validate issuer
        expected_issuer = f"https://{self.settings.auth0_domain}/"
        if payload.get("iss") != expected_issuer:
            raise Auth0SecurityError("Invalid issuer")
        
        # Check expiration
        current_time = time.time()
        if payload.get("exp", 0) <= current_time:
            raise Auth0SecurityError("Token has expired")


# Global validator instance
auth0_validator = Auth0TokenValidator()

# Security dependency
security = HTTPBearer()


def get_auth0_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Get user info from Auth0 token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify token
        payload = auth0_validator.verify_token(credentials.credentials)
        return payload
        
    except Auth0SecurityError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_from_auth0(
    auth0_user: Dict[str, Any] = Depends(get_auth0_user),
    db: Session = Depends(get_db)
):
    """Get or create user from Auth0 token."""
    from ..models.user import User, UserRole
    from ..services.crud import get_user_by_auth0_sub, create_user_from_auth0
    
    # Extract user info from token
    auth0_sub = auth0_user.get("sub")
    email = auth0_user.get("email") or auth0_user.get("https://legaldoc.com/email")
    name = auth0_user.get("name") or auth0_user.get("https://legaldoc.com/name")
    
    if not auth0_sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing subject"
        )
    
    # Try to get existing user
    user = get_user_by_auth0_sub(db, auth0_sub)
    
    if not user:
        # Create new user if doesn't exist
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required for new user creation"
            )
        
        user = create_user_from_auth0(
            db=db,
            auth0_sub=auth0_sub,
            email=email,
            name=name
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def require_admin_auth0(
    current_user = Depends(get_current_user_from_auth0)
):
    """Require admin role for Auth0 authenticated user."""
    from ..models.user import UserRole
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


def get_token_info(
    auth0_user: Dict[str, Any] = Depends(get_auth0_user)
) -> Dict[str, Any]:
    """Get token information for debugging/info purposes."""
    return {
        "sub": auth0_user.get("sub"),
        "email": auth0_user.get("email") or auth0_user.get("https://legaldoc.com/email"),
        "name": auth0_user.get("name") or auth0_user.get("https://legaldoc.com/name"),
        "aud": auth0_user.get("aud"),
        "iss": auth0_user.get("iss"),
        "scope": auth0_user.get("scope"),
        "permissions": auth0_user.get("permissions", [])
    }
