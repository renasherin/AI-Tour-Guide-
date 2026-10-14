"""
Vector Database Service for Incredible Journeys: AI Tour Guide for India.
Manages persistent ChromaDB vector storage and semantic retrieval
with cosine similarity scoring, metadata filtering, and proximity enrichment.
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import chromadb
from chromadb.config import Settings
from backend.app.rag.embeddings import EmbeddingService

logger = logging.getLogger("rag.vector_db")

DEFAULT_CHROMA_DIR = str(Path(__file__).resolve().parent.parent.parent / "data" / "chroma_db")
COLLECTION_NAME = "india_places"

class VectorDBService:
    _instance: Optional["VectorDBService"] = None

    def __new__(cls, persist_directory: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(VectorDBService, cls).__new__(cls)
            cls._instance.persist_dir = persist_directory or os.getenv("CHROMA_PERSIST_DIRECTORY", DEFAULT_CHROMA_DIR)
            cls._instance.embedding_service = EmbeddingService()
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        Path(self.persist_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Initializing persistent ChromaDB at: {self.persist_dir}")
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Connected to collection '{COLLECTION_NAME}' (current count: {self.collection.count()})")

    def count(self) -> int:
        """Return the number of indexed passages."""
        return self.collection.count()

    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: Optional[List[List[float]]] = None, batch_size: int = 100):
        """Index a batch of passages into ChromaDB."""
        if not chunks:
            return

        if embeddings is None:
            texts = [c["text"] for c in chunks]
            embeddings = self.embedding_service.embed_texts(texts)

        for i in range(0, len(chunks), batch_size):
            b_chunks = chunks[i:i + batch_size]
            b_embs = embeddings[i:i + batch_size]

            ids = [c["id"] for c in b_chunks]
            documents = [c["text"] for c in b_chunks]
            
            # Serialize metadata (ChromaDB supports primitive types)
            metadatas = []
            for c in b_chunks:
                meta = {
                    "place_id": str(c.get("place_id", "")),
                    "place": str(c.get("place", "")),
                    "state": str(c.get("state", "")),
                    "city": str(c.get("city", "")),
                    "category": ", ".join(c.get("category", [])) if isinstance(c.get("category"), list) else str(c.get("category", "")),
                    "lat": float(c.get("lat")) if c.get("lat") is not None else 0.0,
                    "lon": float(c.get("lon")) if c.get("lon") is not None else 0.0,
                    "best_time": str(c.get("best_time", "")),
                    "source": str(c.get("source", "")),
                    "source_url": str(c.get("source_url", "")),
                    "google_maps_url": str(c.get("google_maps_url", "")),
                    "directions_url": str(c.get("directions_url", "")),
                    "nearby": json.dumps(c.get("nearby", []), ensure_ascii=False),
                    "chunk_index": int(c.get("chunk_index", 1)),
                    "total_chunks": int(c.get("total_chunks", 1))
                }
                metadatas.append(meta)

            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=b_embs,
                metadatas=metadatas
            )

        logger.info(f"Indexed {len(chunks)} chunks into '{COLLECTION_NAME}'. New total: {self.collection.count()}")

    def search(
        self,
        query: str,
        k: int = 5,
        state: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute semantic similarity search with optional state/category filtering.
        Returns top-k chunks with cosine similarity score in [0.0, 1.0].
        """
        if not query.strip():
            return []

        query_emb = self.embedding_service.embed_query(query)
        
        # Build ChromaDB metadata filter
        where_filter = None
        if state and category:
            where_filter = {
                "$and": [
                    {"state": {"$eq": state}},
                    {"category": {"$contains": category}}
                ]
            }
        elif state:
            where_filter = {"state": {"$eq": state}}
        elif category:
            where_filter = {"category": {"$contains": category}}

        kwargs = {
            "query_embeddings": [query_emb],
            "n_results": min(k, max(1, self.collection.count())),
            "include": ["documents", "metadatas", "distances"]
        }
        if where_filter:
            kwargs["where"] = where_filter

        results = self.collection.query(**kwargs)

        hits = []
        if results and results["ids"] and results["ids"][0]:
            count = len(results["ids"][0])
            for i in range(count):
                doc_id = results["ids"][0][i]
                text = results["documents"][0][i]
                meta = results["metadatas"][0][i]
                dist = results["distances"][0][i] # Cosine distance: 0 is exact match, 2 is opposite

                # Convert cosine distance to cosine similarity in [0, 1]
                similarity = max(0.0, min(1.0, 1.0 - (dist / 2.0)))

                # Parse nearby JSON back
                nearby = []
                try:
                    nearby = json.loads(meta.get("nearby", "[]"))
                except Exception:
                    pass

                category_list = [c.strip() for c in meta.get("category", "").split(",") if c.strip()]

                hits.append({
                    "id": doc_id,
                    "place_id": meta.get("place_id"),
                    "place": meta.get("place"),
                    "state": meta.get("state"),
                    "city": meta.get("city"),
                    "category": category_list,
                    "lat": meta.get("lat"),
                    "lon": meta.get("lon"),
                    "best_time": meta.get("best_time"),
                    "source": meta.get("source"),
                    "source_url": meta.get("source_url"),
                    "google_maps_url": meta.get("google_maps_url", ""),
                    "directions_url": meta.get("directions_url", ""),
                    "nearby": nearby,
                    "text": text,
                    "similarity": round(similarity, 4),
                    "distance": round(dist, 4)
                })

        # Sort descending by similarity
        hits.sort(key=lambda x: x["similarity"], reverse=True)
        return hits
