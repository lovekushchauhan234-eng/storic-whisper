"""
Database-backed memory store for LUPPI 3.0.
Provides persistent storage for conversations, user profiles, and emotional patterns.
"""
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from typing import Optional

from .schemas import SessionMemory
from .models import (
    LuppiConversation,
    LuppiConversationTurn,
    LuppiUserProfile,
    LuppiEmotionalPattern,
    LuppiDomainFrequency,
)

User = get_user_model()


class DatabaseMemoryStore:
    """Database-backed memory for authenticated users."""

    def __init__(self, request: HttpRequest):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None

    def load(self) -> SessionMemory:
        """Load conversation history from database."""
        if not self.user:
            # Fall back to session memory for anonymous users
            from .session import SessionMemoryStore
            return SessionMemoryStore(self.request).load()

        # Get most recent active conversation
        conversation = LuppiConversation.objects.filter(
            user=self.user,
            is_active=True
        ).first()

        if not conversation:
            return SessionMemory(
                session_key=self.request.session.session_key or 'anonymous',
                turns=[],
                used_insight_ids=[],
                domain_counts={},
                emotional_trend=[],
            )

        # Load conversation turns
        from .schemas import ConversationTurn
        turns = []
        for turn in conversation.turns.all()[:24]:  # Last 24 turns
            turns.append(ConversationTurn(
                role=turn.role,
                content=turn.content,
                domain=turn.domain,
                emotion=turn.emotion,
                insight_id=turn.insight_id,
            ))

        # Get used insight IDs
        used_insight_ids = list(
            conversation.turns.filter(insight_id__isnull=False)
            .values_list('insight_id', flat=True)
            .distinct()
        )

        # Get domain counts
        domain_counts = {}
        for freq in conversation.domain_frequencies.all():
            domain_counts[freq.domain] = freq.count

        # Get emotional trend
        emotional_trend = list(
            conversation.emotional_patterns.all()
            .order_by('-timestamp')[:20]
            .values_list('emotion', flat=True)
        )

        return SessionMemory(
            session_key=self.request.session.session_key or 'anonymous',
            turns=turns,
            used_insight_ids=used_insight_ids,
            domain_counts=domain_counts,
            emotional_trend=emotional_trend,
        )

    def save(self, memory: SessionMemory) -> None:
        """Save conversation state to database."""
        if not self.user:
            # Fall back to session memory for anonymous users
            from .session import SessionMemoryStore
            SessionMemoryStore(self.request).save(memory)
            return

        # Get or create active conversation
        conversation, created = LuppiConversation.objects.get_or_create(
            user=self.user,
            is_active=True,
            defaults={
                'session_key': self.request.session.session_key,
                'provider': 'gemini',  # Will be updated based on actual provider
            }
        )

        # Update conversation metadata
        conversation.turn_count = len([t for t in memory.turns if t['role'] == 'user'])
        if memory.domain_counts:
            conversation.primary_domain = max(memory.domain_counts, key=memory.domain_counts.get)
        conversation.save()

    def append_exchange(
        self,
        user_message: str,
        assistant_reply: str,
        domain: str,
        emotion: str,
        insight_id: str | None,
    ) -> SessionMemory:
        """Append a conversation exchange to database."""
        if not self.user:
            # Fall back to session memory for anonymous users
            from .session import SessionMemoryStore
            return SessionMemoryStore(self.request).append_exchange(
                user_message, assistant_reply, domain, emotion, insight_id
            )

        # Get or create active conversation
        conversation, _ = LuppiConversation.objects.get_or_create(
            user=self.user,
            is_active=True,
            defaults={
                'session_key': self.request.session.session_key,
                'provider': 'gemini',
            }
        )

        # Create user turn
        LuppiConversationTurn.objects.create(
            conversation=conversation,
            role='user',
            content=user_message,
            domain=domain,
            emotion=emotion,
        )

        # Create assistant turn
        LuppiConversationTurn.objects.create(
            conversation=conversation,
            role='assistant',
            content=assistant_reply,
            domain=domain,
            emotion=emotion,
            insight_id=insight_id,
        )

        # Update domain frequency
        domain_freq, _ = LuppiDomainFrequency.objects.get_or_create(
            user=self.user,
            session_key=self.request.session.session_key,
            domain=domain,
        )
        domain_freq.count += 1
        domain_freq.save()

        # Record emotional pattern
        LuppiEmotionalPattern.objects.create(
            user=self.user,
            session_key=self.request.session.session_key,
            emotion=emotion,
            domain=domain,
        )

        # Update conversation metadata
        conversation.turn_count += 1
        conversation.save()

        # Return updated memory
        return self.load()

    def get_or_create_profile(self) -> LuppiUserProfile:
        """Get or create user profile."""
        if not self.user:
            raise ValueError("Cannot create profile for anonymous user")

        profile, created = LuppiUserProfile.objects.get_or_create(
            user=self.user,
        )
        return profile

    def update_goals(self, goals: list[str]) -> None:
        """Update user goals in profile."""
        if not self.user:
            return

        profile = self.get_or_create_profile()
        profile.goals = goals
        profile.save()

    def update_struggles(self, struggles: list[str]) -> None:
        """Update user struggles in profile."""
        if not self.user:
            return

        profile = self.get_or_create_profile()
        profile.struggles = struggles
        profile.save()
