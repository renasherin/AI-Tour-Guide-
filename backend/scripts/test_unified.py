import urllib.request
import json
import sys

BASE_URL = "http://localhost:3000"

def test_health():
    url = f"{BASE_URL}/api/health"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode("utf-8"))
    assert data["status"] in ("ok", "healthy"), f"Health status not healthy: {data}"
    print(f"PASS: Health check -> status: {data['status']}, places: {data['vector_db']['collection_count']}")

def test_search(query, expected_min=1):
    url = f"{BASE_URL}/api/destinations?search={urllib.parse.quote(query)}"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode("utf-8"))
    destinations = data.get("destinations", [])
    assert len(destinations) >= expected_min, f"Expected >={expected_min} for '{query}', got {len(destinations)}"
    
    first = destinations[0]
    assert first.get("google_maps_url"), f"Missing google_maps_url in {first['place']}"
    assert "https://www.google.com/maps" in first["google_maps_url"], f"Invalid google_maps_url: {first['google_maps_url']}"
    print(f"PASS: Search '{query}' -> Found {len(destinations)} places. Top: '{first['place']}' (Maps: {first['google_maps_url']})")

def test_detail(slug):
    url = f"{BASE_URL}/api/destinations/{slug}"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode("utf-8"))
    assert data.get("google_maps_url"), f"Missing google_maps_url in {slug}"
    assert data.get("nearby"), f"Missing nearby places in {slug}"
    print(f"PASS: Detail '{slug}' -> '{data['place']}', Maps: {data['google_maps_url']}, Nearby count: {len(data['nearby'])}")

def test_chat():
    url = f"{BASE_URL}/api/chat"
    payload = json.dumps({
        "message": "Tell me about Kozhikode Beach and Vadakara Sandbanks",
        "session_id": "test-verify-session"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    assert len(res["answer"]) > 50, "Chat answer too short"
    assert len(res["sources"]) > 0, "No sources returned"
    for s in res["sources"]:
        assert s.get("google_maps_url"), f"Source {s['place']} missing google_maps_url"
    print(f"PASS: Chat endpoint -> Received answer ({len(res['answer'])} chars) with {len(res['sources'])} source citations and Google Maps links.")

if __name__ == "__main__":
    import urllib.parse
    print("Testing Incredible Journeys Single Localhost Unified Pipeline (http://localhost:3000)...")
    test_health()
    test_search("Kozhikode", 8)
    test_search("Vadakara", 3)
    test_search("Kanjirapuzha", 1)
    test_detail("kanjirapuzha_dam_and_gardens")
    test_detail("kozhikode_beach_and_pier")
    test_detail("lokanarkavu_temple_vadakara")
    test_chat()
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY ON http://localhost:3000!")
