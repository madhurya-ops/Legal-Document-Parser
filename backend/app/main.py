from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import routes
from .api.auth_routes import router as auth_router
from .database import engine
from . import models
from .core.logging_config import setup_logging

# Setup logging
setup_logging()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LegalDoc API", version="1.0.0")

# CORS middleware - simplified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://legaldoc-six.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "LegalDoc API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
