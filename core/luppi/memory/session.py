"""
Session-scoped memory — Django session backend (Phase 1).
Future: DatabaseMemoryStore implementing the same interface.
"""
import json
from dataclasses import asdict

from django.http import HttpRequest

from .base import MemoryStore
from .schemas import ConversationTurn, SessionMemory

SESSION_KEY = 'luppi_memory'
MAX_TURNS = 24


class SessionMemoryStore(MemoryStore):
    def __init__(self, request: HttpRequest, max_turns: int = MAX_TURNS):
        self.request = request
        self.max_turns = max_turns

    def _session_key(self) -> str:
        return self.request.session.session_key or 'anonymous'

    def load(self, session_key: str | None = None) -> SessionMemory:
        raw = self.request.session.get(SESSION_KEY)
        if not raw:
            return SessionMemory(session_key=self._session_key())

        data = json.loads(raw) if isinstance(raw, str) else raw
        turns = [ConversationTurn(**t) for t in data.get('turns', [])]
        return SessionMemory(
            session_key=data.get('session_key', self._session_key()),
            turns=turns[-self.max_turns:],
            used_insight_ids=data.get('used_insight_ids', [])[-50:],
            domain_counts=data.get('domain_counts', {}),
        )

    def save(self, memory: SessionMemory) -> None:
        payload = {
            'session_key': memory.session_key,
            'turns': [asdict(t) for t in memory.turns[-self.max_turns:]],
            'used_insight_ids': memory.used_insight_ids[-50:],
            'domain_counts': memory.domain_counts,
        }
        self.request.session[SESSION_KEY] = json.dumps(payload)
        self.request.session.modified = True

    def append_exchange(
        self,
        user_message: str,
        assistant_reply: str,
        domain: str,
        emotion: str,
        insight_id: str | None,
    ) -> SessionMemory:
        memory = self.load()
        memory.turns.append(ConversationTurn(
            role='user', content=user_message, domain=domain, emotion=emotion,
        ))
        memory.turns.append(ConversationTurn(
            role='assistant',
            content=assistant_reply,
            domain=domain,
            emotion=emotion,
            insight_id=insight_id,
        ))
        if insight_id:
            memory.used_insight_ids.append(insight_id)
        memory.domain_counts[domain] = memory.domain_counts.get(domain, 0) + 1
        self.save(memory)
        return memory

    def recent_user_themes(self, limit: int = 5) -> list[str]:
        memory = self.load()
        return [t.content[:80] for t in memory.turns if t.role == 'user'][-limit:]
