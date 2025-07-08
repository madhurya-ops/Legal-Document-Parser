"""
Configuration Management
=======================

Production-ready configuration system using Pydantic settings.
"""

import os
from functools import lru_cache
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "LegalDoc API"
    debug: bool = False
    version: str = "1.0.0"
    
    # Security (Legacy - will be removed)
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # Auth0 Configuration
    auth0_domain: str
    auth0_audience: str
    
    # Database
    database_url: str
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    # File handling
    upload_directory: str = "./uploads"
    max_file_size: int = 52428800  # 50MB
    allowed_file_types: List[str] = [".pdf", ".doc", ".docx", ".txt"]
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "https://legal-document-parser.vercel.app"
    ]
    allowed_hosts: List[str] = ["*"]
    
    # Vector Store
    vector_store_type: str = "faiss"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Admin
    initial_admin_email: str = "admin@legaldoc.com"
    initial_admin_username: str = "admin"
    initial_admin_password: str = "changeThisPassword123!"
    
    @validator("secret_key")
    def validate_secret_key(cls, v):
        """Validate secret key length."""
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            # Handle JSON string format or comma-separated format
            v = v.strip()
            if v.startswith('[') and v.endswith(']'):
                try:
                    import json
                    return json.loads(v)
                except (json.JSONDecodeError, ValueError):
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    @validator("allowed_hosts", pre=True)
    def parse_allowed_hosts(cls, v):
        """Parse allowed hosts from string or list."""
        if isinstance(v, str):
            # Handle JSON string format or comma-separated format
            v = v.strip()
            if v.startswith('[') and v.endswith(']'):
                try:
                    import json
                    return json.loads(v)
                except (json.JSONDecodeError, ValueError):
                    pass
            return [host.strip() for host in v.split(",") if host.strip()]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
