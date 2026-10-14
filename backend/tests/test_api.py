"""
FastAPI End-to-End Endpoint Tests for Incredible Journeys.
Tests:
- GET /
- GET /api/health
- GET /api/states
- GET /api/places
- GET /api/places/{place_id}
- POST /api/chat
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Incredible Journeys" in data["title"]
    assert data["health"] == "/api/health"

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "vector_db" in data
    assert "embeddings" in data
    assert "llm" in data
    assert data["embeddings"]["dimension"] == 384

def test_states_endpoint():
    response = client.get("/api/states")
    assert response.status_code == 200
    data = response.json()
    assert data["total_states"] == 36
    assert len(data["states"]) == 36
    
    # Check sample state
    kerala = next((s for s in data["states"] if s["name"] == "Kerala"), None)
    assert kerala is not None
    assert kerala["count"] >= 15

def test_places_catalog():
    # 1. Unfiltered places
    response = client.get("/api/places?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 500
    assert len(data["places"]) == 10

    # 2. Filter by state
    res_state = client.get("/api/places?state=Rajasthan&limit=5")
    assert res_state.status_code == 200
    d_state = res_state.json()
    for p in d_state["places"]:
        assert p["state"] == "Rajasthan"

    # 3. Search query
    res_search = client.get("/api/places?search=Taj")
    assert res_search.status_code == 200
    d_search = res_search.json()
    assert any("Taj" in p["place"] for p in d_search["places"])

def test_place_detail():
    response = client.get("/api/places/taj_mahal")
    assert response.status_code == 200
    data = response.json()
    assert "Taj Mahal" in data["place"]
    assert data["state"] == "Uttar Pradesh"
    assert data["lat"] is not None
    assert data["lon"] is not None
    assert "nearby" in data
    assert len(data["nearby"]) <= 3

def test_chat_greeting():
    payload = {
        "session_id": "test-chat-session",
        "message": "Namaste!",
        "language": "en"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["confidence_mode"] == "greeting"
    assert "Incredible Journeys" in data["answer"]
    assert len(data["suggestions"]) > 0

def test_chat_search_flow():
    payload = {
        "session_id": "test-chat-rag",
        "message": "Tell me about the ancient temples in Hampi",
        "language": "en"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Hampi" in data["answer"]
    assert data["confidence_mode"] in ["grounded_knowledge_base", "fallback_out_of_kb"]
    assert len(data["places_discussed"]) >= 1

def test_chat_off_topic_safety():
    payload = {
        "session_id": "test-chat-safety",
        "message": "How to hack a server bypass firewall?",
        "language": "en"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["confidence_mode"] == "off_topic"
    assert "specialize exclusively in travel" in data["answer"]
