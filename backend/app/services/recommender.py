"""
Proactive Recommendation Service for Incredible Journeys: AI Tour Guide for India.
Generates 2-3 intelligent follow-up suggestions for points of interest based on:
- Spatial proximity (Haversine nearby metadata)
- Complementary travel categories (e.g., pairing a heritage fort with local food or nature)
- Current state/region context
- Exclusion of places already discussed in the active session to avoid repetition
"""

import logging
from typing import List, Dict, Any, Set

logger = logging.getLogger("services.recommender")

class RecommendationService:
    def __init__(self):
        pass

    def get_proactive_suggestions(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        discussed_places: Set[str],
        max_suggestions: int = 3
    ) -> List[Dict[str, str]]:
        """
        Produce 2-3 tailored recommendations from retrieved context metadata.
        """
        suggestions = []
        seen_names = set(discussed_places)

        # Strategy 1: Nearby geographical places from retrieved passages
        for chunk in retrieved_chunks:
            primary_place = chunk.get("place", "")
            state = chunk.get("state", "")
            nearby_list = chunk.get("nearby", [])

            for n in nearby_list:
                n_name = n.get("place", "").strip()
                if not n_name or n_name.lower() in [s.lower() for s in seen_names]:
                    continue
                
                dist = n.get("distance_km", 0)
                n_state = n.get("state", state)
                dist_str = f" (~{dist} km away)" if dist > 0 else ""
                
                suggestions.append({
                    "place": n_name,
                    "state": n_state,
                    "prompt": f"Tell me about {n_name} in {n_state}",
                    "reason": f"Close to {primary_place}{dist_str}"
                })
                seen_names.add(n_name)
                if len(suggestions) >= max_suggestions:
                    return suggestions

        # Strategy 2: Alternative places retrieved but not the top-1 primary answer
        for chunk in retrieved_chunks[1:]:
            p_name = chunk.get("place", "").strip()
            state = chunk.get("state", "")
            if not p_name or p_name.lower() in [s.lower() for s in seen_names]:
                continue
                
            categories = chunk.get("category", [])
            cat_str = categories[0] if categories else "highlight"
            suggestions.append({
                "place": p_name,
                "state": state,
                "prompt": f"Tell me about {p_name} in {state}",
                "reason": f"Related {cat_str} destination in {state}"
            })
            seen_names.add(p_name)
            if len(suggestions) >= max_suggestions:
                return suggestions

        # Strategy 3: Default iconic fallback suggestions if history is saturated
        curated_fallbacks = [
            ("Hampi", "Karnataka", "Vijayanagara ruins and boulder landscapes"),
            ("Varanasi Ghats", "Uttar Pradesh", "Ancient spiritual traditions along the holy Ganga"),
            ("Kaziranga National Park", "Assam", "Lush Brahmaputra plains and one-horned rhinos"),
            ("Munnar", "Kerala", "Misty rolling tea gardens in the Western Ghats")
        ]
        
        for name, st, desc in curated_fallbacks:
            if name.lower() not in [s.lower() for s in seen_names]:
                suggestions.append({
                    "place": name,
                    "state": st,
                    "prompt": f"Tell me about {name} in {st}",
                    "reason": desc
                })
                seen_names.add(name)
                if len(suggestions) >= max_suggestions:
                    break

        return suggestions
