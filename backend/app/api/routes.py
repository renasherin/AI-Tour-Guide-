"""
API Routes for Incredible Journeys: AI Tour Guide for India.
Implements:
- POST /api/chat (session_id, message, language)
- POST /api/chat/stream (SSE streaming)
- GET /api/places (filter by state, category, search, pagination)
- GET /api/places/{id} (destination details, nearby places, coords)
- GET /api/states (all 28 states and 8 UTs summary)
- GET /api/health (system health, vector DB status, models)
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from backend.app.rag.vector_db import VectorDBService
from backend.app.services.memory import ConversationMemoryManager
from backend.app.services.query_rewriter import QueryRewriter
from backend.app.services.recommender import RecommendationService
from backend.app.services.llm import LLMService

logger = logging.getLogger("api.routes")
router = APIRouter(prefix="/api")

# Models
class ChatRequest(BaseModel):
    session_id: str = Field(default="default-session", description="Session ID for multi-turn conversational memory")
    message: str = Field(..., description="User question about travel in India")
    language: str = Field(default="en", description="Language code: 'en' for English, 'hi' for Hindi")

class SourceItem(BaseModel):
    place: str
    state: str
    source: str
    source_url: str
    similarity: float

class SuggestionItem(BaseModel):
    place: str
    state: str
    prompt: str
    reason: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    suggestions: List[SuggestionItem]
    confidence_mode: str
    confidence_score: float
    places_discussed: List[str]

# Singletons
memory_manager = ConversationMemoryManager()
query_rewriter = QueryRewriter()
recommender = RecommendationService()
llm_service = LLMService()
vector_db = VectorDBService()

RAW_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """Conversational RAG Chat Endpoint with multi-turn memory and proactive recommendations."""
    raw_message = req.message.strip()
    if not raw_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    session_id = req.session_id
    context = memory_manager.get_context(session_id)
    intent = query_rewriter.classify_intent(raw_message)

    # 1. Handle Greetings
    if intent == "greeting":
        if req.language.lower() == "hi":
            answer = "नमस्ते! मैं 'इंक्रेडिबल जर्नीज़' का आपका निजी टूर गाइड हूँ। भारत के 28 राज्यों और 8 केंद्र शासित प्रदेशों के किसी भी ऐतिहासिक किले, मंदिर, हिल स्टेशन, वन्यजीव या स्थानीय पकवान के बारे में मुझसे पूछें!"
        else:
            answer = "Namaste! Welcome to Incredible Journeys. I am your local AI tour guide for India. Ask me about any of India's 28 states and 8 union territories—from the royal forts of Rajasthan to the serene backwaters of Kerala, ancient temples, or Himalayan trails!"
        
        memory_manager.add_turn(session_id, "user", raw_message)
        memory_manager.add_turn(session_id, "assistant", answer)
        
        default_suggs = recommender.get_proactive_suggestions([], set(context["places_discussed"]))
        return ChatResponse(
            answer=answer,
            sources=[],
            suggestions=[SuggestionItem(**s) for s in default_suggs],
            confidence_mode="greeting",
            confidence_score=1.0,
            places_discussed=context["places_discussed"]
        )

    # 2. Handle Courtesies
    if intent == "courtesy":
        answer = "आपकी यात्रा सुखद और मंगलमय हो! (Wishing you wonderful and safe travels across India!) If you need more recommendations, feel free to ask anytime." if req.language.lower() == "hi" else "You're most welcome! Wishing you wonderful and memorable travels across India. Feel free to ask anytime!"
        memory_manager.add_turn(session_id, "user", raw_message)
        memory_manager.add_turn(session_id, "assistant", answer)
        return ChatResponse(
            answer=answer,
            sources=[],
            suggestions=[],
            confidence_mode="courtesy",
            confidence_score=1.0,
            places_discussed=context["places_discussed"]
        )

    # 3. Handle Off-Topic / Safety Guard
    if intent == "off_topic":
        answer = "As an Incredible Journeys tour guide, I specialize exclusively in travel, culture, heritage, food, and destinations across India's 28 states and 8 union territories. Please ask me a travel-related question!"
        return ChatResponse(
            answer=answer,
            sources=[],
            suggestions=[],
            confidence_mode="off_topic",
            confidence_score=0.0,
            places_discussed=context["places_discussed"]
        )

    # 4. Standard RAG Flow: Query Rewriting
    search_query = query_rewriter.rewrite_query(raw_message, context)

    # 5. Semantic Vector Retrieval
    retrieved_chunks = vector_db.search(search_query, k=5)

    # 6. LLM / Storytelling Generation
    res_data = llm_service.generate_response(
        message=raw_message,
        retrieved_chunks=retrieved_chunks,
        context=context,
        language=req.language
    )

    # 7. Update Session Memory & Discussed Places
    memory_manager.add_turn(session_id, "user", raw_message)
    memory_manager.add_turn(session_id, "assistant", res_data["answer"])
    
    new_places = [c["place"] for c in retrieved_chunks[:2] if c.get("place")]
    memory_manager.record_places(session_id, new_places)
    
    updated_context = memory_manager.get_context(session_id)

    # 8. Generate Proactive Suggestions
    suggestions = recommender.get_proactive_suggestions(
        retrieved_chunks,
        set(updated_context["places_discussed"])
    )

    return ChatResponse(
        answer=res_data["answer"],
        sources=[SourceItem(**s) for s in res_data["sources"]],
        suggestions=[SuggestionItem(**s) for s in suggestions],
        confidence_mode=res_data["confidence_mode"],
        confidence_score=res_data["confidence_score"],
        places_discussed=updated_context["places_discussed"]
    )

@router.post("/chat/stream")
async def chat_stream_endpoint(req: ChatRequest):
    """Server-Sent Events (SSE) streaming chat endpoint."""
    raw_message = req.message.strip()
    session_id = req.session_id
    context = memory_manager.get_context(session_id)
    search_query = query_rewriter.rewrite_query(raw_message, context)
    retrieved_chunks = vector_db.search(search_query, k=5)

    async def event_generator():
        async for token_msg in llm_service.generate_streaming_response(
            raw_message, retrieved_chunks, context, req.language
        ):
            yield token_msg

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/places")
async def get_places(
    state: Optional[str] = Query(None, description="Filter by state or UT"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Text search across place names"),
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Retrieve catalog of destinations with filtering and pagination."""
    files = list(RAW_DATA_DIR.glob("*.json"))
    items = []
    
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as jf:
                data = json.load(jf)
                # Apply filters
                if state and state.lower() != "all" and data.get("state", "").lower() != state.lower():
                    continue
                if category and category.lower() != "all":
                    cats = [c.lower() for c in data.get("category", [])]
                    if not any(category.lower() in c for c in cats):
                        continue
                if search:
                    s_low = search.lower()
                    if s_low not in data.get("place", "").lower() and s_low not in data.get("city", "").lower():
                        continue
                items.append({
                    "id": data.get("id"),
                    "place": data.get("place"),
                    "state": data.get("state"),
                    "city": data.get("city"),
                    "category": data.get("category", []),
                    "best_time": data.get("best_time", ""),
                    "lat": data.get("lat"),
                    "lon": data.get("lon"),
                    "wikipedia_url": data.get("wikipedia_url", "")
                })
        except Exception:
            continue

    items.sort(key=lambda x: x["place"])
    total = len(items)
    paginated = items[offset:offset + limit]

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "places": paginated
    }

@router.get("/places/{place_id}")
async def get_place_detail(place_id: str):
    """Retrieve detailed metadata for a single destination."""
    file_path = RAW_DATA_DIR / f"{place_id}.json"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Place '{place_id}' not found.")
        
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Find 3 nearby destinations
    nearby = []
    plat, plon = data.get("lat"), data.get("lon")
    if plat and plon:
        for other_file in RAW_DATA_DIR.glob("*.json"):
            if other_file.stem == place_id:
                continue
            try:
                with open(other_file, "r", encoding="utf-8") as of:
                    o = json.load(of)
                    olat, olon = o.get("lat"), o.get("lon")
                    if olat and olon:
                        from backend.scripts.chunker import haversine
                        dist = haversine(plat, plon, olat, olon)
                        nearby.append({
                            "id": o.get("id"),
                            "place": o.get("place"),
                            "state": o.get("state"),
                            "distance_km": dist
                        })
            except Exception:
                continue
        nearby.sort(key=lambda x: x["distance_km"])
        data["nearby"] = nearby[:3]

    return data

@router.get("/states")
async def get_states():
    """Summary of all 28 States and 8 Union Territories with counts."""
    files = list(RAW_DATA_DIR.glob("*.json"))
    state_map: Dict[str, Dict[str, Any]] = {}
    
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as jf:
                d = json.load(jf)
                st = d.get("state", "India")
                if st not in state_map:
                    state_map[st] = {
                        "name": st,
                        "count": 0,
                        "sample_places": []
                    }
                state_map[st]["count"] += 1
                if len(state_map[st]["sample_places"]) < 4:
                    state_map[st]["sample_places"].append(d.get("place"))
        except Exception:
            continue

    states_list = sorted(list(state_map.values()), key=lambda x: x["name"])
    return {
        "total_states": len(states_list),
        "states": states_list
    }

@router.get("/health")
async def get_health():
    """System health inspection endpoint."""
    return {
        "status": "ok",
        "service": "Incredible Journeys API",
        "vector_db": {
            "collection_count": vector_db.count(),
            "collection_name": "india_places",
            "persist_dir": vector_db.persist_dir
        },
        "embeddings": {
            "model_name": vector_db.embedding_service.model_name,
            "dimension": vector_db.embedding_service.dimension
        },
        "llm": {
            "model_name": llm_service.model_name,
            "api_key_configured": bool(llm_service.api_key),
            "similarity_threshold": llm_service.similarity_threshold
        }
    }
