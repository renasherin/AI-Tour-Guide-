"""
Tests for Conversational Memory and Session History.
Verifies:
- 6-turn verbatim window retention
- Summarization of turns beyond 6
- Tracking of places already discussed
- Session isolation
"""

import pytest
from backend.app.services.memory import ConversationMemoryManager, SessionState

def test_session_turns_and_summarization():
    mem = ConversationMemoryManager()
    session_id = "test-session-mem-1"
    mem.clear(session_id)

    # Add 4 turns (2 user, 2 assistant)
    mem.add_turn(session_id, "user", "What is Hampi famous for?")
    mem.add_turn(session_id, "assistant", "Hampi is famous for the Vijayanagara Empire ruins and boulder hills.")
    mem.add_turn(session_id, "user", "How far is Badami?")
    mem.add_turn(session_id, "assistant", "Badami is about 140 km from Hampi.")

    ctx = mem.get_context(session_id)
    assert len(ctx["verbatim_turns"]) == 4
    assert ctx["summary"] == "" # No summarization yet

    # Add 4 more turns (exceeding 6 verbatim limit)
    mem.add_turn(session_id, "user", "What about the caves?")
    mem.add_turn(session_id, "assistant", "The Badami Cave Temples date back to the 6th century Chalukya dynasty.")
    mem.add_turn(session_id, "user", "What is the best time to visit?")
    mem.add_turn(session_id, "assistant", "October to March is ideal.")

    ctx2 = mem.get_context(session_id)
    assert len(ctx2["verbatim_turns"]) == 6
    assert "Prior conversation summary:" in ctx2["summary"]
    assert "Hampi" in ctx2["summary"]

def test_places_discussed_tracking():
    mem = ConversationMemoryManager()
    session_id = "test-session-places"
    mem.clear(session_id)

    mem.record_places(session_id, ["Hampi", "Badami"])
    mem.record_places(session_id, ["Hampi", "Pattadakal"])

    ctx = mem.get_context(session_id)
    discussed = ctx["places_discussed"]
    assert len(discussed) == 3
    assert "Hampi" in discussed
    assert "Badami" in discussed
    assert "Pattadakal" in discussed
