"""
ChromaDB Indexing Pipeline for Incredible Journeys: AI Tour Guide for India.
Reads processed chunks from data/processed/chunks.jsonl, computes multilingual embeddings,
and indexes them persistently into ChromaDB with rich metadata.
"""

import sys
import json
import time
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.rag.vector_db import VectorDBService

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("indexer")

CHUNKS_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "chunks.jsonl"

def run_indexer():
    if not CHUNKS_FILE.exists():
        logger.error(f"Chunks file not found at {CHUNKS_FILE}. Run chunker.py first!")
        return

    logger.info(f"Loading chunks from {CHUNKS_FILE}...")
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    logger.info(f"Loaded {len(chunks)} chunks ready for vector indexing.")

    # Initialize Vector DB
    db = VectorDBService()
    
    start_time = time.time()
    logger.info(f"Embedding and indexing {len(chunks)} chunks in batches...")
    
    db.add_chunks(chunks, batch_size=64)
    
    elapsed = time.time() - start_time
    logger.info(f"Successfully indexed all {len(chunks)} chunks in {elapsed:.2f} seconds ({len(chunks)/elapsed:.1f} chunks/sec)!")
    logger.info(f"Total documents in ChromaDB collection: {db.count()}")

if __name__ == "__main__":
    run_indexer()
