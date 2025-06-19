from fastapi import FastAPI
from app.api import routes

app = FastAPI()

app.include_router(routes.router)
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
