"""
Tests for Grounding, Fallback Tiers, and Proactive Suggestions.
Verifies:
- Grounded answers when similarity exceeds threshold
- Fallback tier when similarity is below threshold
- Labeling of 'from general knowledge, less verified'
- Proactive recommendations using proximity and history deduplication
"""

import pytest
from backend.app.services.llm import LLMService
from backend.app.services.recommender import RecommendationService

def test_grounded_answer_generation():
    llm = LLMService()
    retrieved_chunks = [
        {
            "place": "Hampi",
            "state": "Karnataka",
            "city": "Vijayanagara",
            "category": ["heritage", "temples"],
            "best_time": "October to March",
            "similarity": 0.82,
            "raw_passage": "Hampi is a UNESCO World Heritage Site in east-central Karnataka. It was the capital of the Vijayanagara Empire in the 14th century.",
            "source": "Wikipedia (CC BY-SA 4.0)"
        }
    ]
    context = {"verbatim_turns": [], "places_discussed": []}

    res = llm.generate_response("Tell me about Hampi", retrieved_chunks, context, language="en")
    assert res["confidence_mode"] == "grounded_knowledge_base"
    assert res["confidence_score"] == 0.82
    assert len(res["sources"]) == 1
    assert "Hampi" in res["answer"]
    assert "Karnataka" in res["answer"]

def test_fallback_out_of_kb():
    llm = LLMService()
    # Below similarity threshold
    low_sim_chunks = [
        {
            "place": "Random Place",
            "state": "Unknown",
            "category": [],
            "similarity": 0.12,
            "raw_passage": "",
            "source": ""
        }
    ]
    context = {"verbatim_turns": [], "places_discussed": []}

    res = llm.generate_response("Where can I find penguins in the Sahara desert?", low_sim_chunks, context, language="en")
    assert res["confidence_mode"] == "fallback_out_of_kb"
    assert "from general knowledge, less verified" in res["answer"]
    assert "not covered in our curated Incredible Journeys guidebook" in res["answer"]

def test_proactive_recommendations():
    rec = RecommendationService()
    retrieved_chunks = [
        {
            "place": "Hampi",
            "state": "Karnataka",
            "nearby": [
                {"place": "Pattadakal", "state": "Karnataka", "distance_km": 115.0},
                {"place": "Badami Cave Temples", "state": "Karnataka", "distance_km": 120.0},
                {"place": "Aihole", "state": "Karnataka", "distance_km": 110.0}
            ]
        }
    ]
    
    # Pattadakal is already discussed in session
    discussed = {"Pattadakal"}
    suggestions = rec.get_proactive_suggestions(retrieved_chunks, discussed, max_suggestions=2)

    # Pattadakal should be filtered out
    sugg_names = [s["place"] for s in suggestions]
    assert "Pattadakal" not in sugg_names
    assert "Badami Cave Temples" in sugg_names
    assert len(suggestions) <= 2
