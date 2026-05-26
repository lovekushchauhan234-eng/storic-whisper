"""
Memory schemas — future-ready structures for persistent LUPPI memory.
Not persisted to DB yet; used by session store and future migrations.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ConversationTurn:
    role: str  # 'user' | 'assistant'
    content: str
    domain: str = 'general'
    emotion: str = 'neutral'
    insight_id: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class EmotionalPattern:
    """Aggregated emotional signals across sessions (future)."""
    tone_counts: dict[str, int] = field(default_factory=dict)
    recurring_themes: list[str] = field(default_factory=list)
    last_primary_tone: str = 'neutral'


@dataclass
class UserMemoryProfile:
    """
    Future persistent profile — goals, struggles, boundaries user has named.
    """
    user_id: str | None = None
    goals: list[str] = field(default_factory=list)
    struggles: list[str] = field(default_factory=list)
    preferred_language: str = 'hi-en'
    emotional_pattern: EmotionalPattern = field(default_factory=EmotionalPattern)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionMemory:
    """In-session memory (Django session today; DB later)."""
    session_key: str
    turns: list[ConversationTurn] = field(default_factory=list)
    used_insight_ids: list[str] = field(default_factory=list)
    domain_counts: dict[str, int] = field(default_factory=dict)
