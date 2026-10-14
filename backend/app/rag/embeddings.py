"""
Embedding Service for Incredible Journeys: AI Tour Guide for India.
Uses sentence-transformers with 'paraphrase-multilingual-MiniLM-L12-v2'
to provide high-quality multilingual embeddings (supporting English, Hindi, and Indian regional languages).
"""

import os
import logging
from typing import List, Optional
import numpy as np

logger = logging.getLogger("rag.embeddings")

DEFAULT_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

class EmbeddingService:
    _instance: Optional["EmbeddingService"] = None
    _model = None
    
    def __new__(cls, model_name: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance.model_name = model_name or os.getenv("EMBEDDING_MODEL", DEFAULT_MODEL_NAME)
            cls._instance._load_model()
        return cls._instance
        
    def _load_model(self):
        logger.info(f"Loading embedding model: {self.model_name}...")
        try:
            from sentence_transformers import SentenceTransformer
            try:
                self._model = SentenceTransformer(self.model_name, local_files_only=True)
            except Exception:
                self._model = SentenceTransformer(self.model_name)
            logger.info(f"Embedding model '{self.model_name}' successfully loaded into memory.")
        except Exception as e:
            logger.error(f"Failed to load SentenceTransformer model '{self.model_name}': {e}")
            raise e

    def embed_texts(self, texts: List[str], batch_size: int = 64) -> List[List[float]]:
        """Compute embeddings for a batch of text passages."""
        if not texts:
            return []
        if self._model is None:
            self._load_model()
        embeddings = self._model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True
        )
        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        """Compute embedding for a single search query."""
        if self._model is None:
            self._load_model()
        emb = self._model.encode(
            [query],
            show_progress_bar=False,
            normalize_embeddings=True
        )[0]
        return emb.tolist()

    @property
    def dimension(self) -> int:
        """Embedding vector dimension (384 for MiniLM-L12-v2)."""
        return 384
