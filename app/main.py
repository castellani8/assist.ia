import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.route.api import router as ask_router

load_dotenv()

app = FastAPI(
    title="Assist.IA API",
    description="An AI assistant API powered by Google's Gemini model",
    version="1.0.0"
)

# Configure CORS with specific origins
origins = [
    "http://localhost:3000",  # React default port
    "http://localhost:8000",  # FastAPI default port
    # Add your production domains here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve index.html at the root
@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")

# Add the main router
app.include_router(ask_router, prefix="", tags=["ask"])