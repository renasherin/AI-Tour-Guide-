"""
RAG Generator for Incredible Journeys: AI Tour Guide for India.
Coordinates grounded generation, strict attribution formatting,
SSE streaming events, and proactive suggestion chips.
"""

import json
import logging
import asyncio
from typing import List, Dict, Any, Optional, AsyncIterator

from backend.app.services.llm import LLMService
from backend.app.services.recommender import RecommendationService
from backend.app.rag.retriever import RAGRetriever

logger = logging.getLogger("rag.generator")

class RAGGenerator:
    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        retriever: Optional[RAGRetriever] = None,
        recommender: Optional[RecommendationService] = None
    ):
        self.llm_service = llm_service or LLMService()
        self.retriever = retriever or RAGRetriever()
        self.recommender = recommender or RecommendationService()

    async def stream_rag_chat(
        self,
        query: str,
        session_id: str,
        language: str = "en",
        context: Optional[Dict[str, Any]] = None
    ) -> AsyncIterator[str]:
        """
        Execute 3-step RAG flow and yield SSE events:
        Step 1: Normalized semantic retrieval
        Step 2: Context injection with citation attribution
        Step 3: Streaming tokens + structured events for sources and follow-up suggestions
        """
        context = context or {"places_discussed": [], "summary": "", "verbatim_turns": []}
        
        # Step 1: Query normalization & semantic retrieval
        retrieved_chunks = self.retriever.retrieve(query, k=5)
        sources_metadata = self.retriever.format_sources_metadata(retrieved_chunks)

        # Step 2: Emit initial 'sources' event immediately so UI can display citation badges
        yield f"event: sources\ndata: {json.dumps(sources_metadata, ensure_ascii=False)}\n\n"

        # Generate response using LLM service (or high-quality grounded local generator)
        res_data = self.llm_service.generate_response(
            message=query,
            retrieved_chunks=retrieved_chunks,
            context=context,
            language=language
        )
        answer_text = res_data.get("answer", "")

        # Step 3: Stream tokens
        words = answer_text.split(" ")
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            payload = json.dumps({"token": chunk, "done": False}, ensure_ascii=False)
            yield f"data: {payload}\n\n"
            await asyncio.sleep(0.018)

        # Generate follow-up suggestions
        discussed_places = set(context.get("places_discussed", []))
        suggestions = self.recommender.get_proactive_suggestions(retrieved_chunks, discussed_places)

        # Emit suggestions event
        yield f"event: suggestions\ndata: {json.dumps(suggestions, ensure_ascii=False)}\n\n"

        # Emit final completion done event
        final_payload = json.dumps({
            "done": True,
            "confidence_mode": res_data.get("confidence_mode", "grounded_knowledge_base"),
            "confidence_score": res_data.get("confidence_score", 0.95),
            "sources": sources_metadata,
            "suggestions": suggestions
        }, ensure_ascii=False)
        yield f"data: {final_payload}\n\n"
