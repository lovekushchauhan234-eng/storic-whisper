"""
Emotional context layer — detects tone/state from user message (session-scale, not clinical).
"""
from dataclasses import dataclass
from enum import Enum

from .text_utils import term_in_text


class EmotionalTone(str, Enum):
    GRIEF = 'grief'
    ATTACHMENT = 'attachment'
    ANGER = 'anger'
    LONELINESS = 'loneliness'
    CONFUSION = 'confusion'
    SHAME = 'shame'
    NUMB = 'numb'
    ANXIETY = 'anxiety'
    NEUTRAL = 'neutral'


@dataclass
class EmotionalContext:
    primary: EmotionalTone
    intensity: float  # 0.0–1.0 heuristic
    signals: list[str]


_EMOTION_PATTERNS: list[tuple[EmotionalTone, list[str], float]] = [
    (EmotionalTone.GRIEF, [
        'दर्द', 'dard', 'रो', 'ro raha', 'cry', 'miss', 'याद', 'grief', 'खो', 'lost', 'टूट', 'broken', 'heartbreak',
    ], 1.0),
    (EmotionalTone.ATTACHMENT, [
        'attach', 'bond', 'छोड़', 'वापस', 'contact', 'याद', 'addict', 'छोड़कर', 'वापसी',
    ], 0.9),
    (EmotionalTone.ANGER, [
        'गुस्सा', 'anger', 'hate', 'नफरत', 'cheat', 'धोखा', 'betray',
    ], 0.85),
    (EmotionalTone.LONELINESS, [
        'अकेला', 'alone', 'lonely', 'कोई नहीं', 'empty', 'खाली',
    ], 0.9),
    (EmotionalTone.CONFUSION, [
        'confus', 'समझ', 'क्यों', 'why', 'mixed', 'signal', 'पता नहीं',
    ], 0.75),
    (EmotionalTone.SHAME, [
        'shame', 'शर्म', 'गिल्ट', 'guilty', 'weak', 'कमजोर', 'loser',
    ], 0.85),
    (EmotionalTone.NUMB, [
        'numb', 'कुछ feel', 'feel नहीं', 'empty', 'dead inside', 'सुन्न',
    ], 0.8),
    (EmotionalTone.ANXIETY, [
        'anxiety', 'panic', 'घबर', 'overthink', 'सो नहीं', "can't sleep",
    ], 0.85),
]


def analyze_emotion(message: str) -> EmotionalContext:
    text = message.lower()
    scores: dict[EmotionalTone, float] = {}

    for tone, keywords, weight in _EMOTION_PATTERNS:
        hits = sum(1 for kw in keywords if term_in_text(kw, text))
        if hits:
            scores[tone] = scores.get(tone, 0) + hits * weight

    if not scores:
        return EmotionalContext(EmotionalTone.NEUTRAL, 0.0, [])

    primary = max(scores, key=scores.get)
    intensity = min(1.0, scores[primary] / 3.0)
    signals = [t.value for t in scores.keys()]

    return EmotionalContext(primary, intensity, signals)
