"""
Foods and Culinary Heritage Router for Incredible Journeys.
Provides:
- GET /api/foods (filter by state, region, veg/non-veg, category, search)
- GET /api/foods/{id} (detailed food item)
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["Culinary Heritage"])

FOODS_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "foods.json"

def load_all_foods() -> List[Dict[str, Any]]:
    if not FOODS_FILE.exists():
        return []
    try:
        with open(FOODS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

@router.get("/api/foods")
async def get_foods(
    state: Optional[str] = Query(None, description="Filter by state"),
    region: Optional[str] = Query(None, description="Filter by geographic region"),
    category: Optional[str] = Query(None, description="Filter by category (Biryani, Street Food, etc.)"),
    is_veg: Optional[bool] = Query(None, description="Filter by vegetarian status"),
    search: Optional[str] = Query(None, description="Search term across food name, ingredients, or story"),
    limit: int = Query(50, ge=1, le=100)
):
    foods = load_all_foods()
    filtered = []

    for f in foods:
        if state and state.lower() != "all" and f.get("state", "").lower() != state.lower():
            continue
        if region and region.lower() != "all" and f.get("region", "").lower() != region.lower():
            continue
        if category and category.lower() != "all" and f.get("category", "").lower() != category.lower():
            continue
        if is_veg is not None and f.get("is_veg") != is_veg:
            continue
        if search:
            s_low = search.lower()
            text_corpus = f"{f.get('name', '')} {f.get('native_name', '')} {f.get('flavor_profile', '')} {f.get('story', '')} {f.get('best_places_to_try', '')}".lower()
            if s_low not in text_corpus:
                continue
        filtered.append(f)

    return {
        "total": len(filtered),
        "foods": filtered[:limit]
    }

@router.get("/api/foods/{food_id}")
async def get_food_detail(food_id: str):
    foods = load_all_foods()
    for f in foods:
        if f.get("id") == food_id or f.get("id").replace("_", "-") == food_id:
            return f
    raise HTTPException(status_code=404, detail=f"Food item '{food_id}' not found.")
