"""
Unit tests for RAG chunking, normalization, and semantic retrieval.
"""

import pytest
from backend.app.rag.retriever import RAGRetriever

def test_query_normalization():
    retriever = RAGRetriever()
    dirty_query = "   Where can I find @#$ Hampi ruins in Karnataka???   "
    clean = retriever.normalize_query(dirty_query)
    assert clean == "Where can I find Hampi ruins in Karnataka???"

def test_retriever_source_formatting():
    retriever = RAGRetriever()
    sample_chunks = [
        {
            "place": "Hampi",
            "state": "Karnataka",
            "category": ["heritage", "unesco"],
            "source_url": "https://en.wikipedia.org/wiki/Hampi",
            "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
            "raw_passage": "Hampi is an ancient village in Karnataka dotted with ruins. It was the capital of the Vijayanagara Empire.",
            "similarity": 0.88,
            "lat": 15.335,
            "lon": 76.46
        }
    ]
    formatted = retriever.format_sources_metadata(sample_chunks)
    assert len(formatted) == 1
    src = formatted[0]
    assert src["title"] == "Hampi"
    assert src["place"] == "Hampi"
    assert src["state"] == "Karnataka"
    assert "Vijayanagara" in src["excerpt"]
    assert src["license"] == "Wikipedia & Wikivoyage (CC BY-SA 4.0)"
    assert src["similarity"] == 0.88

def test_retriever_search_execution():
    retriever = RAGRetriever()
    results = retriever.retrieve("golden temple amritsar", k=3)
    assert len(results) > 0
    top = results[0]
    assert "place" in top
    assert "similarity" in top
    assert top["similarity"] > 0.0
