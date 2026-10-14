"""
Unit & Integration Tests for Destinations and Regional Coverage.
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "vector_db" in data
    assert data["vector_db"]["collection_count"] > 0
    assert "region_coverage" in data
    assert data["region_coverage"]["states_covered"] == 28
    assert data["region_coverage"]["union_territories_covered"] == 8

def test_get_destinations_pagination():
    res = client.get("/api/destinations?limit=10&page=1")
    assert res.status_code == 200
    data = res.json()
    assert "destinations" in data
    assert len(data["destinations"]) <= 10
    assert data["total"] > 100

def test_get_destinations_state_filter():
    res = client.get("/api/destinations?state=Kerala&limit=5")
    assert res.status_code == 200
    data = res.json()
    assert len(data["destinations"]) > 0
    for d in data["destinations"]:
        assert d["state"] == "Kerala"

def test_get_destinations_unesco_filter():
    res = client.get("/api/destinations?unesco=true&limit=5")
    assert res.status_code == 200
    data = res.json()
    assert len(data["destinations"]) > 0
    for d in data["destinations"]:
        assert d["is_unesco"] is True

def test_get_destination_detail_taj_mahal():
    res = client.get("/api/destinations/taj_mahal")
    assert res.status_code == 200
    data = res.json()
    assert data["place"] == "Taj Mahal"
    assert data["state"] == "Uttar Pradesh"
    assert data["lat"] is not None
    assert data["lon"] is not None
    assert "nearby" in data

def test_get_regions_metadata_all_36():
    res = client.get("/api/metadata/regions")
    assert res.status_code == 200
    data = res.json()
    assert data["total_divisions"] == 36
    assert data["states_count"] == 28
    assert data["union_territories_count"] == 8
