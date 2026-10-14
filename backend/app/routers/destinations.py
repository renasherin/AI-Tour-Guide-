"""
Destinations and Regional Metadata Router for Incredible Journeys.
Endpoints:
- GET /api/destinations (filterable by state, category, unesco status, search, pagination)
- GET /api/destinations/{slug} (deep dive details, coordinates, license attribution, nearby)
- GET /api/metadata/regions (all 36 administrative divisions with counts & signatures)
- GET /api/places (alias for backwards compatibility)
- GET /api/places/{slug} (alias)
- GET /api/states (alias)
"""

import json
import logging
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["Destinations & Geography"])
logger = logging.getLogger("routers.destinations")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
REGIONS_FILE = DATA_DIR / "india_regions.json"

def generate_google_maps_url(place: str, state: str, city: str = "", lat: Optional[float] = None, lon: Optional[float] = None) -> str:
    """Generate universal Google Maps search or pin URL."""
    if lat is not None and lon is not None and float(lat) != 0.0 and float(lon) != 0.0:
        return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    query = f"{place}, {city + ', ' if city else ''}{state}, India"
    return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(query)}"

def generate_directions_url(place: str, state: str = "", lat: Optional[float] = None, lon: Optional[float] = None) -> str:
    """Generate Google Maps turn-by-turn directions URL."""
    if lat is not None and lon is not None and float(lat) != 0.0 and float(lon) != 0.0:
        return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
    query = f"{place}, {state}" if state else place
    return f"https://www.google.com/maps/dir/?api=1&destination={urllib.parse.quote_plus(query)}"

def calculate_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in km between two coordinate pairs."""
    import math
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

def load_all_destinations() -> List[Dict[str, Any]]:
    """Load all destination profile JSON files from data/raw."""
    destinations = []
    if not RAW_DATA_DIR.exists():
        return destinations
    
    for f in RAW_DATA_DIR.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as jf:
                data = json.load(jf)
                destinations.append(data)
        except Exception:
            continue
    return destinations

@router.get("/api/destinations")
@router.get("/api/places")
async def get_destinations(
    state: Optional[str] = Query(None, description="Filter by state or Union Territory name"),
    category: Optional[str] = Query(None, description="Filter by category (heritage, nature, food, temples, etc.)"),
    unesco: Optional[bool] = Query(None, description="Filter only UNESCO World Heritage Sites"),
    search: Optional[str] = Query(None, description="Search keyword across place name, city, or overview"),
    page: Optional[int] = Query(None, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(24, ge=1, le=100, description="Items per page"),
    offset: Optional[int] = Query(None, ge=0, description="Offset for pagination")
):
    """
    Retrieve destinations with rich filtering, search, and pagination.
    """
    destinations = load_all_destinations()
    filtered = []

    for d in destinations:
        # State filter
        if state and state.lower() != "all":
            if d.get("state", "").lower() != state.lower():
                continue

        # Category filter
        cats = [c.lower() for c in d.get("category", [])]
        if category and category.lower() != "all":
            c_target = category.lower()
            if not any(c_target in c for c in cats):
                continue

        # UNESCO filter
        if unesco is not None:
            text = (d.get("text", "") + " " + " ".join(cats)).lower()
            is_unesco = any("unesco" in c for c in cats) or "unesco" in text or "world heritage" in text
            if unesco and not is_unesco:
                continue
            if not unesco and is_unesco:
                continue

        # Search filter
        if search:
            s_low = search.lower()
            match_place = s_low in d.get("place", "").lower()
            match_city = s_low in d.get("city", "").lower()
            match_state = s_low in d.get("state", "").lower()
            match_text = s_low in d.get("text", "")[:300].lower()
            if not (match_place or match_city or match_state or match_text):
                continue

        # Extract verified summary
        cats_list = d.get("category", [])
        is_unesco_flag = any("unesco" in c.lower() for c in cats_list) or "unesco" in d.get("text", "").lower()

        filtered.append({
            "id": d.get("id"),
            "slug": d.get("id"),
            "place": d.get("place"),
            "title": d.get("place"),
            "state": d.get("state"),
            "city": d.get("city"),
            "category": cats_list,
            "best_time": d.get("best_time", ""),
            "lat": d.get("lat"),
            "lon": d.get("lon"),
            "latitude": d.get("lat"),
            "longitude": d.get("lon"),
            "image_url": d.get("image_url", ""),
            "google_maps_url": d.get("google_maps_url") or generate_google_maps_url(d.get("place", ""), d.get("state", ""), d.get("city", ""), d.get("lat"), d.get("lon")),
            "directions_url": d.get("directions_url") or generate_directions_url(d.get("place", ""), d.get("state", ""), d.get("lat"), d.get("lon")),
            "is_unesco": is_unesco_flag,
            "source_url": d.get("source_url", d.get("wikipedia_url", "")),
            "attribution": d.get("attribution", "CC BY-SA 4.0"),
            "excerpt": (d.get("text", "")[:260] + "...") if len(d.get("text", "")) > 260 else d.get("text", "")
        })

    # Sort deterministically
    filtered.sort(key=lambda x: x["place"])
    total = len(filtered)

    # Handle page vs offset
    if page is not None:
        calc_offset = (page - 1) * limit
    elif offset is not None:
        calc_offset = offset
    else:
        calc_offset = 0

    paginated = filtered[calc_offset:calc_offset + limit]

    return {
        "total": total,
        "offset": calc_offset,
        "limit": limit,
        "page": (calc_offset // limit) + 1,
        "total_pages": (total + limit - 1) // limit if total > 0 else 1,
        "destinations": paginated,
        "places": paginated  # backwards-compatible key
    }

@router.get("/api/destinations/{slug}")
@router.get("/api/places/{slug}")
async def get_destination_detail(slug: str):
    """
    Retrieve verified deep-dive destination details, coordinates, attribution, and nearby places.
    """
    file_path = RAW_DATA_DIR / f"{slug}.json"
    if not file_path.exists():
        # Try matching by slug against all place ids
        matched_file = None
        for f in RAW_DATA_DIR.glob("*.json"):
            if f.stem.lower() == slug.lower() or f.stem.replace("_", "-").lower() == slug.lower():
                matched_file = f
                break
        if not matched_file:
            raise HTTPException(status_code=404, detail=f"Destination '{slug}' not found.")
        file_path = matched_file

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Compute neighboring places if coordinates exist
    plat, plon = data.get("lat"), data.get("lon")
    nearby = []
    
    all_places = load_all_destinations()
    if plat and plon:
        for other in all_places:
            if other.get("id") == data.get("id"):
                continue
            olat, olon = other.get("lat"), other.get("lon")
            if olat and olon:
                dist = calculate_haversine(plat, plon, olat, olon)
                nearby.append({
                    "id": other.get("id"),
                    "slug": other.get("id"),
                    "place": other.get("place"),
                    "state": other.get("state"),
                    "city": other.get("city"),
                    "category": other.get("category", []),
                    "distance_km": dist,
                    "lat": olat,
                    "lon": olon,
                    "image_url": other.get("image_url", ""),
                    "google_maps_url": other.get("google_maps_url") or generate_google_maps_url(other.get("place", ""), other.get("state", ""), other.get("city", ""), olat, olon),
                    "directions_url": other.get("directions_url") or generate_directions_url(other.get("place", ""), other.get("state", ""), olat, olon)
                })
        nearby.sort(key=lambda x: x["distance_km"])
        data["nearby"] = nearby[:3]
    else:
        # Fallback to same-state recommendations if coordinates are unverified/null
        same_state = [
            {
                "id": o.get("id"),
                "slug": o.get("id"),
                "place": o.get("place"),
                "state": o.get("state"),
                "city": o.get("city"),
                "category": o.get("category", []),
                "distance_km": None,
                "image_url": o.get("image_url", ""),
                "google_maps_url": o.get("google_maps_url") or generate_google_maps_url(o.get("place", ""), o.get("state", ""), o.get("city", ""), o.get("lat"), o.get("lon")),
                "directions_url": o.get("directions_url") or generate_directions_url(o.get("place", ""), o.get("state", ""), o.get("lat"), o.get("lon"))
            }
            for o in all_places
            if o.get("state") == data.get("state") and o.get("id") != data.get("id")
        ]
        data["nearby"] = same_state[:3]

    # Add normalized fields
    data["slug"] = data.get("id")
    data["latitude"] = data.get("lat")
    data["longitude"] = data.get("lon")
    data["image_url"] = data.get("image_url", "")
    data["google_maps_url"] = data.get("google_maps_url") or generate_google_maps_url(data.get("place", ""), data.get("state", ""), data.get("city", ""), plat, plon)
    data["directions_url"] = data.get("directions_url") or generate_directions_url(data.get("place", ""), data.get("state", ""), plat, plon)
    cats = data.get("category", [])
    data["is_unesco"] = any("unesco" in c.lower() for c in cats) or "unesco" in data.get("text", "").lower()

    return data

@router.get("/api/metadata/regions")
@router.get("/api/states")
async def get_regions_metadata():
    """
    Return all 36 administrative divisions (28 States & 8 Union Territories)
    with total destination counts, signature experiences, and metadata.
    """
    all_places = load_all_destinations()
    
    # Load region profiles if available
    region_info_map = {}
    if REGIONS_FILE.exists():
        try:
            with open(REGIONS_FILE, "r", encoding="utf-8") as rf:
                reg_data = json.load(rf)
                for div in reg_data.get("divisions", []):
                    region_info_map[div["name"]] = div
        except Exception as e:
            logger.warning(f"Failed to load regions file: {e}")

    # Aggregate counts by state
    state_map: Dict[str, Dict[str, Any]] = {}
    for p in all_places:
        st = p.get("state", "India")
        if st not in state_map:
            meta = region_info_map.get(st, {})
            state_map[st] = {
                "name": st,
                "type": meta.get("type", "State" if "Territory" not in st else "Union Territory"),
                "capital": meta.get("capital", p.get("city", "")),
                "zone": meta.get("zone", "India"),
                "tagline": meta.get("tagline", "Discover the wonders of this region"),
                "unesco_sites": meta.get("unesco_sites", []),
                "count": 0,
                "sample_places": []
            }
        state_map[st]["count"] += 1
        if len(state_map[st]["sample_places"]) < 5:
            state_map[st]["sample_places"].append(p.get("place"))

    # Include any division that might have 0 places
    for div_name, meta in region_info_map.items():
        if div_name not in state_map:
            state_map[div_name] = {
                "name": div_name,
                "type": meta.get("type", "State"),
                "capital": meta.get("capital", ""),
                "zone": meta.get("zone", "India"),
                "tagline": meta.get("tagline", ""),
                "unesco_sites": meta.get("unesco_sites", []),
                "count": 0,
                "sample_places": []
            }

    sorted_divisions = sorted(list(state_map.values()), key=lambda x: x["name"])

    states_only = [d for d in sorted_divisions if d.get("type") == "State"]
    uts_only = [d for d in sorted_divisions if d.get("type") != "State"]

    return {
        "total_divisions": len(sorted_divisions),
        "total_states": len(sorted_divisions),
        "states_count": len(states_only),
        "union_territories_count": len(uts_only),
        "divisions": sorted_divisions,
        "states": sorted_divisions  # backwards-compatible
    }
