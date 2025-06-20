from fastapi import FastAPI
from app.api import routes

app = FastAPI()

app.include_router(routes.router)
from fastapi.middleware.cors import CORSMiddleware
# Allow only production frontend and localhost for dev
origins = [
    "http://localhost:3000",  # local dev
    "http://127.0.0.1:3000",
    "https://your-vercel-app.vercel.app"  # <-- replace with your actual Vercel domain
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
