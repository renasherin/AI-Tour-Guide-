"""
Conversation Memory Service for Incredible Journeys: AI Tour Guide for India.
Manages per-session multi-turn dialogue history:
- Retains the last 6 turns verbatim
- Summarizes older turns to preserve context without bloating prompt tokens
- Tracks 'places_already_discussed' to avoid repetition and enable contextual follow-ups
"""

import time
import logging
from typing import List, Dict, Set, Optional, Any

logger = logging.getLogger("services.memory")

class SessionState:
    def __init__(self, session_id: str):
        self.session_id: str = session_id
        self.turns: List[Dict[str, Any]] = []
        self.summary: str = ""
        self.places_discussed: Set[str] = set()
        self.created_at: float = time.time()
        self.updated_at: float = time.time()

    def add_turn(self, role: str, content: str):
        self.turns.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        self.updated_at = time.time()
        
        # When history exceeds 6 turns (3 complete roundtrips), summarize older turns
        if len(self.turns) > 6:
            older_turn = self.turns.pop(0)
            role_label = "Traveler" if older_turn["role"] == "user" else "Guide"
            # Append brief summary item
            compact = f"{role_label}: {older_turn['content'][:90]}... "
            if not self.summary:
                self.summary = "Prior conversation summary: " + compact
            else:
                self.summary += compact
                if len(self.summary) > 400:
                    self.summary = self.summary[-400:]

    def add_discussed_places(self, places: List[str]):
        for p in places:
            if p and isinstance(p, str):
                self.places_discussed.add(p.strip())

    def get_history_for_prompt(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "verbatim_turns": self.turns[-6:],
            "places_discussed": sorted(list(self.places_discussed))
        }

class ConversationMemoryManager:
    _instance: Optional["ConversationMemoryManager"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConversationMemoryManager, cls).__new__(cls)
            cls._instance.sessions: Dict[str, SessionState] = {}
        return cls._instance

    def get_session(self, session_id: str) -> SessionState:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(session_id)
        return self.sessions[session_id]

    def add_turn(self, session_id: str, role: str, content: str):
        session = self.get_session(session_id)
        session.add_turn(role, content)

    def record_places(self, session_id: str, places: List[str]):
        session = self.get_session(session_id)
        session.add_discussed_places(places)

    def get_context(self, session_id: str) -> Dict[str, Any]:
        session = self.get_session(session_id)
        return session.get_history_for_prompt()

    def clear(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
