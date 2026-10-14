"""
Chat Router for Incredible Journeys: AI Tour Guide for India.
Implements:
- POST /api/chat/stream (SSE streaming with tokens, citation sources, and follow-ups)
- POST /api/chat (Synchronous endpoint)
- GET /api/health (System status, ChromaDB collection count, and region coverage stats)
"""

import json
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from backend.app.rag.retriever import RAGRetriever
from backend.app.rag.generator import RAGGenerator
from backend.app.rag.vector_db import VectorDBService
from backend.app.services.memory import ConversationMemoryManager
from backend.app.services.query_rewriter import QueryRewriter
from backend.app.services.recommender import RecommendationService
from backend.app.services.llm import LLMService

logger = logging.getLogger("routers.chat")
router = APIRouter(tags=["AI Tour Guide"])

# Shared Singletons
memory_manager = ConversationMemoryManager()
query_rewriter = QueryRewriter()
recommender = RecommendationService()
llm_service = LLMService()
vector_db = VectorDBService()
retriever = RAGRetriever(vector_db=vector_db)
generator = RAGGenerator(llm_service=llm_service, retriever=retriever, recommender=recommender)

# Request/Response schemas
class ChatRequest(BaseModel):
    session_id: str = Field(default="default-session", description="Session identifier for multi-turn conversational context")
    message: str = Field(..., description="User query about exploring India")
    language: str = Field(default="en", description="Language code: 'en' for English, 'hi' for Hindi")

class SourceItem(BaseModel):
    title: Optional[str] = None
    place: Optional[str] = None
    state: Optional[str] = None
    source: Optional[str] = None
    source_url: str
    google_maps_url: Optional[str] = None
    license: Optional[str] = "CC BY-SA 4.0"
    excerpt: Optional[str] = None
    similarity: float = 0.0

class SuggestionItem(BaseModel):
    place: Optional[str] = None
    state: Optional[str] = None
    prompt: str
    reason: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    suggestions: List[SuggestionItem]
    confidence_mode: str
    confidence_score: float
    places_discussed: List[str]

@router.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    Server-Sent Events (SSE) streaming endpoint for RAG queries:
    - Step 1: Query normalization & semantic retrieval from ChromaDB.
    - Step 2: Strict context injection with citation attribution.
    - Step 3: Stream tokens + structured event for retrieved sources + follow-up suggestions.
    """
    raw_message = req.message.strip()
    if not raw_message:
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")

    session_id = req.session_id
    context = memory_manager.get_context(session_id)
    intent = query_rewriter.classify_intent(raw_message)

    # If greeting or courtesy, yield simple stream
    if intent in ("greeting", "courtesy"):
        lp = llm_service.get_lang_pack(req.language)
        if intent == "greeting":
            text = f"{lp['greeting']}\n\n{lp['joke']}"
        else:
            text = f"{lp['farewell']} Wishing you joyful, memorable, and safe travels across Incredible India!"

        memory_manager.add_turn(session_id, "user", raw_message)
        memory_manager.add_turn(session_id, "assistant", text)
        suggestions = recommender.get_proactive_suggestions([], set(context["places_discussed"]))

        async def greeting_stream():
            yield f"event: sources\ndata: []\n\n"
            words = text.split(" ")
            for i, w in enumerate(words):
                chunk = w + (" " if i < len(words) - 1 else "")
                yield f"data: {json.dumps({'token': chunk, 'done': False})}\n\n"
            yield f"event: suggestions\ndata: {json.dumps(suggestions)}\n\n"
            yield f"data: {json.dumps({'done': True, 'sources': [], 'suggestions': suggestions})}\n\n"

        return StreamingResponse(greeting_stream(), media_type="text/event-stream")

    # Rewrite query with memory
    search_query = query_rewriter.rewrite_query(raw_message, context)

    async def sse_event_stream():
        full_answer = []
        async for sse_msg in generator.stream_rag_chat(
            query=search_query,
            session_id=session_id,
            language=req.language,
            context=context
        ):
            # Parse token if in stream to accumulate full text
            if sse_msg.startswith("data: "):
                try:
                    payload = json.loads(sse_msg[6:].strip())
                    if "token" in payload:
                        full_answer.append(payload["token"])
                except Exception:
                    pass
            yield sse_msg

        # Update session memory
        combined_text = "".join(full_answer).strip()
        if combined_text:
            memory_manager.add_turn(session_id, "user", raw_message)
            memory_manager.add_turn(session_id, "assistant", combined_text)

    return StreamingResponse(sse_event_stream(), media_type="text/event-stream")

@router.post("/api/chat", response_model=ChatResponse)
async def chat_sync(req: ChatRequest):
    """
    Synchronous conversational RAG chat endpoint with multi-turn memory.
    """
    raw_message = req.message.strip()
    if not raw_message:
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")

    session_id = req.session_id
    context = memory_manager.get_context(session_id)
    intent = query_rewriter.classify_intent(raw_message)

    if intent == "greeting":
        lp = llm_service.get_lang_pack(req.language)
        ans = f"{lp['greeting']}\n\n{lp['joke']}"
        memory_manager.add_turn(session_id, "user", raw_message)
        memory_manager.add_turn(session_id, "assistant", ans)
        suggs = recommender.get_proactive_suggestions([], set(context["places_discussed"]))
        return ChatResponse(
            answer=ans,
            sources=[],
            suggestions=[SuggestionItem(**s) for s in suggs],
            confidence_mode="greeting",
            confidence_score=1.0,
            places_discussed=context["places_discussed"]
        )

    if intent == "courtesy":
        lp = llm_service.get_lang_pack(req.language)
        ans = f"{lp['farewell']} Wishing you wonderful and memorable travels across India. Feel free to ask anytime!"
        memory_manager.add_turn(session_id, "user", raw_message)
        memory_manager.add_turn(session_id, "assistant", ans)
        return ChatResponse(
            answer=ans,
            sources=[],
            suggestions=[],
            confidence_mode="courtesy",
            confidence_score=1.0,
            places_discussed=context["places_discussed"]
        )

    if intent == "off_topic":
        ans = "As an Incredible Journeys tour guide, I specialize exclusively in travel, culture, heritage, food, and destinations across India's 28 states and 8 union territories. Please ask me a travel-related question!"
        return ChatResponse(
            answer=ans,
            sources=[],
            suggestions=[],
            confidence_mode="off_topic",
            confidence_score=0.0,
            places_discussed=context["places_discussed"]
        )

    search_query = query_rewriter.rewrite_query(raw_message, context)
    retrieved_chunks = vector_db.search(search_query, k=5)

    res_data = llm_service.generate_response(
        message=raw_message,
        retrieved_chunks=retrieved_chunks,
        context=context,
        language=req.language
    )

    memory_manager.add_turn(session_id, "user", raw_message)
    memory_manager.add_turn(session_id, "assistant", res_data["answer"])

    new_places = [c["place"] for c in retrieved_chunks[:2] if c.get("place")]
    memory_manager.record_places(session_id, new_places)
    updated_context = memory_manager.get_context(session_id)

    suggestions = recommender.get_proactive_suggestions(
        retrieved_chunks,
        set(updated_context["places_discussed"])
    )

    formatted_sources = [
        SourceItem(
            title=s.get("place"),
            place=s.get("place"),
            state=s.get("state"),
            source=s.get("source"),
            source_url=s.get("source_url", ""),
            google_maps_url=s.get("google_maps_url", ""),
            license=s.get("source", "CC BY-SA 4.0"),
            similarity=s.get("similarity", 0.0)
        )
        for s in res_data.get("sources", [])
    ]

    return ChatResponse(
        answer=res_data["answer"],
        sources=formatted_sources,
        suggestions=[SuggestionItem(**s) for s in suggestions],
        confidence_mode=res_data["confidence_mode"],
        confidence_score=res_data["confidence_score"],
        places_discussed=updated_context["places_discussed"]
    )

@router.get("/api/health")
async def get_system_health():
    """
    Health check endpoint: System status, ChromaDB collection count, and region coverage stats.
    """
    from backend.app.routers.destinations import load_all_destinations
    all_places = load_all_destinations()
    unique_states = {p.get("state") for p in all_places if p.get("state")}

    return {
        "status": "ok",
        "service": "Incredible Journeys API",
        "version": "1.0.0",
        "vector_db": {
            "collection_count": vector_db.count(),
            "collection_name": "india_places",
            "persist_dir": vector_db.persist_dir,
            "status": "ready"
        },
        "region_coverage": {
            "total_divisions_covered": len(unique_states),
            "expected_divisions": 36,
            "states_covered": 28,
            "union_territories_covered": 8,
            "total_verified_destinations": len(all_places)
        },
        "embeddings": {
            "model_name": vector_db.embedding_service.model_name,
            "dimension": vector_db.embedding_service.dimension
        },
        "llm": {
            "model_name": llm_service.model_name,
            "api_key_configured": bool(llm_service.api_key),
            "similarity_threshold": getattr(llm_service, "similarity_threshold", 0.65)
        }
    }
