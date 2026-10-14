"""
Semantic & Live Multi-Source Retriever for Incredible Journeys: AI Tour Guide for India.
Retrieves from:
1. Local Vector Database (639 verified destinations across 36 states/UTs)
2. Authentic Regional Foods Atlas (foods.json)
3. Live Wikipedia & OpenData APIs (for off-seed places, cultural events, and hidden gems)
"""

import re
import json
import logging
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Dict, Any, Optional

from backend.app.rag.vector_db import VectorDBService

logger = logging.getLogger("rag.retriever")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FOODS_FILE = BASE_DIR / "data" / "foods.json"

class RAGRetriever:
    def __init__(self, vector_db: Optional[VectorDBService] = None):
        self.vector_db = vector_db or VectorDBService()
        self.foods = self._load_foods()

    def _load_foods(self) -> List[Dict[str, Any]]:
        if not FOODS_FILE.exists():
            return []
        try:
            with open(FOODS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load foods.json: {e}")
            return []

    def normalize_query(self, query: str) -> str:
        """Clean and normalize query string for semantic vector search."""
        cleaned = re.sub(r"[^\w\s\-,.?!]", "", query.strip())
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    def search_foods(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Search local authentic foods atlas matching query keywords."""
        q_low = query.lower()
        matched = []
        for food in self.foods:
            name = food.get("name", "").lower()
            native = food.get("native_name", "").lower()
            state = food.get("state", "").lower()
            cat = food.get("category", "").lower()
            profile = food.get("flavor_profile", "").lower()

            score = 0
            # Direct dish name match
            for word in q_low.split():
                if len(word) > 3:
                    if word in name or word in native:
                        score += 3
                    elif word in state or word in cat:
                        score += 2
                    elif word in profile:
                        score += 1

            # Keyword triggers
            if any(k in q_low for k in ["food", "dish", "eat", "cuisine", "taste", "snack", "sweet", "biryani", "roti", "curry", "halwa", "chokha", "kulcha", "dosa"]):
                if state in q_low or any(w in name for w in q_low.split()):
                    score += 2

            if score > 0:
                matched.append((score, food))

        matched.sort(key=lambda x: x[0], reverse=True)
        results = []
        for _, f in matched[:limit]:
            fname = f.get("name", "")
            fstate = f.get("state", "")
            food_query = f"{fname} {fstate} India"
            results.append({
                "place": fname,
                "food_name": fname,
                "native_name": f.get("native_name"),
                "state": fstate,
                "city": f.get("best_places_to_try", ""),
                "category": ["Food", f.get("category", "Culinary Heritage")],
                "best_time": "Year-round",
                "image_url": f.get("image_url", ""),
                "source": "Incredible Journeys Culinary Atlas (CC BY-SA 4.0)",
                "source_url": "https://en.wikipedia.org/wiki/Indian_cuisine",
                "google_maps_url": f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(food_query)}",
                "text": f"[{fname} ({f.get('native_name')}) - {fstate}]: {f.get('flavor_profile')}. {f.get('story')} Best places to try: {f.get('best_places_to_try')}. Perfect pairing: {f.get('pairing')}.",
                "raw_passage": f"{f.get('flavor_profile')}. {f.get('story')} Best places to try: {f.get('best_places_to_try')}. Pair with: {f.get('pairing')}.",
                "similarity": 0.89,
                "is_food": True
            })
        return results

    def fetch_live_wikipedia(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Query live Wikipedia Action API for unindexed landmarks, off-seed temples,
        or historical figures across India.
        """
        # Strip common travel filler phrases
        clean_term = re.sub(
            r"(?i)\b(tell me about|what is the history of|where is|how to visit|famous places in|best time to visit|near|food of|show me|history of)\b",
            "",
            query
        ).strip()
        if not clean_term or len(clean_term) < 3:
            clean_term = query.strip()

        search_str = f"{clean_term} India"
        api_url = (
            "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts|coordinates|info|pageimages"
            f"&inprop=url&exintro=1&explaintext=1&piprop=thumbnail&pithumbsize=1000"
            f"&generator=search&gsrsearch={urllib.parse.quote(search_str)}&gsrlimit=1"
        )
        try:
            req = urllib.request.Request(
                api_url,
                headers={"User-Agent": "IncredibleJourneysAI/2.0 (travel@incrediblejourneys.in)"}
            )
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                for _, page in pages.items():
                    title = page.get("title")
                    extract = page.get("extract", "")
                    if not extract or len(extract) < 50:
                        continue
                    full_url = page.get("fullurl", f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title)}")
                    thumb = page.get("thumbnail", {}).get("source", "")
                    coords = page.get("coordinates", [{}])[0]
                    lat = coords.get("lat")
                    lon = coords.get("lon")

                    gmaps_url = ""
                    if lat and lon:
                        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                    else:
                        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(f'{title}, India')}"

                    return {
                        "place": title,
                        "state": "India",
                        "city": "",
                        "category": ["Heritage", "Live Wikipedia Intelligence"],
                        "best_time": "October to March",
                        "image_url": thumb,
                        "source": "Wikipedia Open API (CC BY-SA 4.0)",
                        "source_url": full_url,
                        "google_maps_url": gmaps_url,
                        "text": f"[{title} - India]: {extract}",
                        "raw_passage": extract,
                        "similarity": 0.84,
                        "lat": lat,
                        "lon": lon,
                        "is_live_wiki": True
                    }
        except Exception as e:
            logger.debug(f"Live Wikipedia lookup skipped or timed out: {e}")
        return None

    def retrieve(
        self,
        query: str,
        k: int = 5,
        state: Optional[str] = None,
        category: Optional[str] = None,
        unesco_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Perform comprehensive multi-tier retrieval:
        1. Local vector database (639 destinations)
        2. Foods atlas if culinary query
        3. Live Wikipedia open API if local similarity is low
        """
        norm_query = self.normalize_query(query)
        results = self.vector_db.search(
            query=norm_query,
            k=k * 2 if unesco_only else k,
            state=state,
            category=category
        )

        if unesco_only:
            filtered = []
            for item in results:
                cats = [c.lower() for c in item.get("category", [])]
                text = (item.get("raw_passage", "") + " " + item.get("text", "")).lower()
                if any("unesco" in c for c in cats) or "world heritage" in text or "unesco" in text:
                    filtered.append(item)
            results = filtered

        # Check for food queries
        food_results = self.search_foods(query, limit=2)
        if food_results:
            # Prepend or blend relevant food items
            combined = food_results + results
            results = combined[:k]

        # If similarity of top result is low (< 0.50), trigger live Wikipedia discovery
        top_score = results[0].get("similarity", 0.0) if results else 0.0
        if top_score < 0.50 or not results:
            live_item = self.fetch_live_wikipedia(query)
            if live_item:
                results.insert(0, live_item)

        return results[:k]

    def format_sources_metadata(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format retrieved items into strict citation source objects."""
        sources = []
        for c in chunks:
            raw_text = c.get("raw_passage", c.get("text", "")).strip()
            sentences = [s.strip() for s in raw_text.split(".") if len(s.strip()) > 15]
            excerpt = ". ".join(sentences[:2]) + "." if sentences else raw_text[:200]

            lat = c.get("lat")
            lon = c.get("lon")
            place = c.get("place", "Destination in India")
            state = c.get("state", "India")
            
            gmaps_url = c.get("google_maps_url", "")
            if not gmaps_url:
                if lat and lon and float(lat) != 0.0 and float(lon) != 0.0:
                    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                else:
                    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(f'{place}, {state}, India')}"

            sources.append({
                "title": place,
                "place": place,
                "state": state,
                "category": c.get("category", []),
                "source_url": c.get("source_url", "https://en.wikipedia.org"),
                "google_maps_url": gmaps_url,
                "license": c.get("source", "CC BY-SA 4.0"),
                "excerpt": excerpt,
                "similarity": c.get("similarity", 0.0),
                "image_url": c.get("image_url", ""),
                "lat": lat,
                "lon": lon
            })
        return sources
