"""
Response composer — human layer first, optional psychological depth.
"""
from ..classifier import ClassificationResult
from ..emotional import EmotionalContext, EmotionalTone
from ..intent import ResponseDepth
from ..personality import EMOTIONAL_OPENERS


def compose_reply(
    natural_body: str,
    insight_body: str | None = None,
    depth: ResponseDepth = ResponseDepth.NONE,
    emotion: EmotionalContext | None = None,
    *,
    force_ack: bool = False,
) -> str:
    """
    natural_body: conversational core (always shown)
    insight_body: optional psychology (LIGHT/FULL only, when relevant)
    """
    parts: list[str] = [natural_body.strip()]

    if depth == ResponseDepth.NONE:
        return parts[0]

    # LIGHT/FULL: optional emotional ack only when not already in natural_body
    if force_ack and emotion and emotion.primary != EmotionalTone.NEUTRAL:
        if emotion.intensity >= 0.4:
            opener = EMOTIONAL_OPENERS.get(emotion.primary.value, EMOTIONAL_OPENERS['default'])
            if opener not in parts[0]:
                parts.insert(0, opener)

    if insight_body and depth in (ResponseDepth.LIGHT, ResponseDepth.FULL):
        insight = insight_body.strip()
        if depth == ResponseDepth.LIGHT:
            from ..conversational import trim_insight_for_light
            insight = trim_insight_for_light(insight, max_sentences=2)
        if insight and insight not in parts[0]:
            parts.append(insight)

    return '\n\n'.join(parts)
