"""
Configuration settings for Incredible Journeys: AI Tour Guide for India backend.
"""

import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CHROMA_DIR = DATA_DIR / "chroma_db"
REGIONS_FILE = DATA_DIR / "india_regions.json"
MANIFEST_FILE = DATA_DIR / "seed_manifest.json"

class Settings(BaseModel):
    # Model settings
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
    
    # RAG settings
    chroma_persist_dir: str = str(CHROMA_DIR)
    collection_name: str = "india_places"
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.35"))
    top_k: int = int(os.getenv("TOP_K", "5"))
    
    # Server settings
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    cors_origins: list[str] = [
        o.strip()
        for o in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
        if o.strip()
    ]

settings = Settings()
