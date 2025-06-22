from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import routes
from .api.auth_routes import router as auth_router
from .database import engine
from . import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LegalDoc API",
    description="API for Legal Document Processing with Authentication",
    version="1.0.0"
)

# CORS middleware configuration
origins = [
    "http://localhost:3000",  # local dev
    "http://127.0.0.1:3000",
    "https://legaldoc-six.vercel.app"  # production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to LegalDoc API with Authentication"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "LegalDoc API"}
