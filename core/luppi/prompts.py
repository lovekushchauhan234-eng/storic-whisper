"""
Structured prompt assembly — for LLM providers (Gemini, Claude, local models).
"""
from .classifier import ClassificationResult
from .domains import Domain
from .emotional import EmotionalContext
from .memory.schemas import SessionMemory
from .personality import LUPPI_IDENTITY, RESPONSE_RULES


def build_system_prompt() -> str:
    """Build system prompt with LUPPI personality and Socratic questioning (optimized for tokens)."""
    return f"""{LUPPI_IDENTITY.strip()}

Style:
- Socratic questioning, not lecturing
- Conversational, explore and understand
- Adapt to emotional state
- Hindi-English mix natural

Socratic:
- Ask "what/how" not "why"
- Help user discover insights
- Probe assumptions gently
- Encourage self-reflection

Response:
1. Acknowledge and validate
2. Explore through questioning
3. Offer insight if relevant
4. Ask one follow-up
Keep concise (2-3 paragraphs)."""


def build_user_context_block(
    message: str,
    classification: ClassificationResult,
    emotion: EmotionalContext,
    memory: SessionMemory | None = None,
) -> str:
    lines = [
        f'User message: {message}',
        f'Primary domain: {classification.domain.value} (confidence {classification.confidence})',
        f'Emotional tone: {emotion.primary.value} (intensity {emotion.intensity:.2f})',
    ]
    if memory and memory.turns:
        recent = memory.turns[-6:]
        lines.append('Recent conversation:')
        for t in recent:
            prefix = 'User' if t.role == 'user' else 'LUPPI'
            lines.append(f'  {prefix}: {t.content[:200]}')
    if memory and memory.domain_counts:
        lines.append(f'Domain frequency this session: {memory.domain_counts}')
    if memory and hasattr(memory, 'emotional_trend') and memory.emotional_trend:
        lines.append(f'Emotional trend: {memory.emotional_trend[-5:]}')
    lines.append(f'Response rules: max_paragraphs={RESPONSE_RULES["max_paragraphs"]}')
    return '\n'.join(lines)


def build_full_prompt(
    message: str,
    insight_body: str,
    classification: ClassificationResult,
    emotion: EmotionalContext,
    memory: SessionMemory | None = None,
) -> dict[str, str]:
    """
    Returns messages[]-shaped dict for API providers.
    """
    return {
        'system': build_system_prompt(),
        'context': build_user_context_block(message, classification, emotion, memory),
        'knowledge_injection': (
            f'Use this psychological core (expand in LUPPI voice, do not copy verbatim):\n{insight_body}'
        ),
        'user': message,
    }
