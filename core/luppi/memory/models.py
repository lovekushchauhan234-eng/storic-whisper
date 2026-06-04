"""
Database models for LUPPI 3.0 advanced memory system.
Provides persistent storage for conversations, user profiles, and emotional patterns.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LuppiConversation(models.Model):
    """Individual conversation sessions with LUPPI."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='luppi_conversations'
    )
    session_key = models.CharField(max_length=255, null=True, blank=True)  # For anonymous users
    provider = models.CharField(max_length=20, default='local')  # local, anthropic, gemini
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    turn_count = models.IntegerField(default=0)
    primary_domain = models.CharField(max_length=50, default='general')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
            models.Index(fields=['started_at']),
        ]

    def __str__(self):
        user_id = self.user.id if self.user else 'anonymous'
        return f"Conversation {self.id} (User: {user_id})"


class LuppiConversationTurn(models.Model):
    """Individual message turns within a conversation."""

    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'LUPPI'),
    ]

    conversation = models.ForeignKey(
        LuppiConversation,
        on_delete=models.CASCADE,
        related_name='turns'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    domain = models.CharField(max_length=50, default='general')
    emotion = models.CharField(max_length=50, default='neutral')
    insight_id = models.CharField(max_length=100, null=True, blank=True)
    intent = models.CharField(max_length=50, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class LuppiUserProfile(models.Model):
    """User profiles for personalized LUPPI experience."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='luppi_profile'
    )
    preferred_language = models.CharField(max_length=10, default='hi-en')
    preferred_response_style = models.CharField(
        max_length=20,
        choices=[
            ('mechanism', 'Mechanism-focused'),
            ('supportive', 'Supportive'),
            ('direct', 'Direct'),
        ],
        default='mechanism'
    )
    goals = models.JSONField(default=list, blank=True)  # List of user goals
    struggles = models.JSONField(default=list, blank=True)  # List of recurring struggles
    interests = models.JSONField(default=list, blank=True)  # Topics of interest
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"Profile for {self.user.username}"


class LuppiEmotionalPattern(models.Model):
    """Track emotional patterns across conversations."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='emotional_patterns'
    )
    session_key = models.CharField(max_length=255, null=True, blank=True)
    emotion = models.CharField(max_length=50)
    intensity = models.FloatField(default=0.0)
    domain = models.CharField(max_length=50, default='general')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
            models.Index(fields=['emotion']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.emotion} ({self.intensity}) - {self.timestamp}"


class LuppiDomainFrequency(models.Model):
    """Track domain frequency per user for personalization."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='domain_frequencies'
    )
    session_key = models.CharField(max_length=255, null=True, blank=True)
    domain = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'session_key', 'domain']]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['domain']),
        ]

    def __str__(self):
        return f"{self.domain}: {self.count}"
