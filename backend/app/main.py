from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging
from .api import routes
from .api.auth_routes import router as auth_router
from .api.admin_routes import router as admin_router
from .api.legal_routes import router as legal_router
from .api.chat_routes import router as chat_router
from .database import engine
from . import models
from .core.logging_config import setup_logging
from .exceptions import AppException

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting up LegalDoc API v2.0")
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    logger.info("Shutting down LegalDoc API")

app = FastAPI(
    title="LegalDoc API",
    version="2.0.0",
    description="AI-powered legal document analysis platform with modern architecture and advanced features",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware - updated origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://legaldoc-six.vercel.app",
        "https://legaldoc-bansalchaitanya1234-2881s-projects.vercel.app",
        "https://legal-document-parser.vercel.app",
        "https://legal-document-parser-kpgy5779l-madhuryas-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(routes.router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(legal_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "LegalDoc API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
# update Sun Jul  6 02:54:59 IST 2025
# update Sun Jul  6 02:56:34 IST 2025
