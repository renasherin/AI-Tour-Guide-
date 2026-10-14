"""
FastAPI Application Entry Point for Incredible Journeys: AI Tour Guide for India.
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from backend.app.routers.chat import router as chat_router
from backend.app.routers.destinations import router as destinations_router
from backend.app.routers.foods import router as foods_router
from backend.app.api.routes import router as legacy_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main")

app = FastAPI(
    title="Incredible Journeys: Discover India with AI",
    description="Conversational RAG Tour Guide & Curated Atlas covering all 28 states and 8 union territories of India.",
    version="1.0.0"
)

# CORS configuration
origins_env = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
cors_origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(destinations_router)
app.include_router(foods_router)

from fastapi.responses import RedirectResponse
from fastapi import Request

@app.get("/")
def root(request: Request):
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        return RedirectResponse(url="http://localhost:3000/", status_code=307)
    return {
        "title": "Incredible Journeys: AI Tour Guide for India",
        "description": "Production RAG API for travel exploration across India.",
        "documentation": "/docs",
        "health": "/api/health",
        "web_app": "http://localhost:3000"
    }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=True)
