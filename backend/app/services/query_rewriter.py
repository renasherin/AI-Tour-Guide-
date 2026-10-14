"""
Query Rewriting and Intent Classification Service for Incredible Journeys.
- Handles greetings and conversational small-talk directly without retrieval
- Detects off-topic queries and prompt injection attempts
- Rewrites pronouns and elliptical follow-ups (e.g. 'what about food there?') into standalone search queries
"""

import re
import logging
from typing import Tuple, Dict, Any, Optional, List

logger = logging.getLogger("services.query_rewriter")

GREETING_PATTERNS = [
    r"^(hi|hello|hey|namaste|namaskar|pranam|good\s+(morning|afternoon|evening|day)|greetings)[\s!.,?]*$",
    r"^(नमस्ते|नमस्कार|प्रणाम|जय\s+श्री\s+राम|राधे\s+राधे)[\s!.,?]*$",
    r"^(who\s+are\s+you|what\s+can\s+you\s+do|introduce\s+yourself)[\s!.,?]*$",
    r"^(तुम\s+कौन\s+हो|आप\s+कौन\s+हैं)[\s!.,?]*$"
]

COURTESY_PATTERNS = [
    r"^(thanks|thank\s+you|thank\s+you\s+so\s+much|thanks\s+a\s+lot|dhanyawad|shukriya|bye|goodbye|see\s+you)[\s!.,?]*$",
    r"^(धन्यवाद|बहुत\s+धन्यवाद|शुक्रिया|अलविदा)[\s!.,?]*$",
    r"\b(thank\s+you\s+so\s+much|thanks\s+a\s+lot)\b"
]

OFF_TOPIC_KEYWORDS = [
    "python code", "write a script", "stock market", "crypto", "bitcoin",
    "hack", "bypass", "system prompt", "ignore previous instructions",
    "jailbreak", "dan mode", "nuclear", "bomb", "sql injection"
]

class QueryRewriter:
    def __init__(self):
        pass

    def classify_intent(self, message: str) -> str:
        """Classifies message intent into: 'greeting', 'courtesy', 'off_topic', 'search'."""
        cleaned = message.strip().lower()

        # Check prompt injection or off-topic
        for bad in OFF_TOPIC_KEYWORDS:
            if bad in cleaned:
                return "off_topic"

        # Check greetings
        for pat in GREETING_PATTERNS:
            if re.search(pat, cleaned, re.IGNORECASE):
                return "greeting"

        # Check courtesies
        for pat in COURTESY_PATTERNS:
            if re.search(pat, cleaned, re.IGNORECASE):
                return "courtesy"

        return "search"

    def rewrite_query(self, message: str, context: Dict[str, Any]) -> str:
        """
        Rewrites conversational follow-up questions into standalone search queries.
        e.g., If last discussed place is 'Hampi' and user asks 'what about food there?',
        rewrites to 'Hampi food and cuisine Karnataka'.
        """
        text = message.strip()
        lower = text.lower()
        
        # Check if query contains pronouns or elliptical references
        referential_cues = [
            "there", "this place", "that place", "the place", "it",
            "यहाँ", "वहाँ", "इस जगह", "उस जगह", "यहाँ का", "वहाँ का",
            "food there", "how to reach", "best time", "how to visit", "hotels", "weather"
        ]
        
        has_cue = any(cue in lower for cue in referential_cues) or len(text.split()) <= 4
        
        # Get recently discussed places from memory
        places_discussed = context.get("places_discussed", [])
        last_turn_assistant = ""
        verbatim = context.get("verbatim_turns", [])
        for t in reversed(verbatim):
            if t["role"] == "assistant":
                last_turn_assistant = t["content"]
                break

        # If user asks a follow-up and we have an anchor place
        if (has_cue or "what about" in lower or "tell me more" in lower) and places_discussed:
            anchor_place = places_discussed[-1] # Most recent place
            
            # Remove vague referents
            cleaned_query = re.sub(r"\b(there|this place|that place|it|यहाँ|वहाँ)\b", "", text, flags=re.IGNORECASE).strip()
            
            # Construct reformulated standalone query
            reformulated = f"{anchor_place} {cleaned_query}".strip()
            logger.info(f"Rewrote follow-up query: '{message}' -> '{reformulated}' (Anchor: {anchor_place})")
            return reformulated

        return text
