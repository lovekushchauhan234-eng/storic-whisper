"""
Conversation intent — runs BEFORE domain classification.
Prioritizes literal message understanding over psychology routing.
"""
from dataclasses import dataclass
from enum import Enum
import re

from .memory.schemas import SessionMemory
from .text_utils import term_in_text


class ConversationIntent(str, Enum):
    GREETING = 'greeting'
    SMALL_TALK = 'small_talk'
    EMOTIONAL_CHECKIN = 'emotional_checkin'
    RELATIONSHIP = 'relationship'
    STUDY_FOCUS = 'study_focus'
    LONELINESS = 'loneliness'
    DEEP_PSYCHOLOGY = 'deep_psychology'
    AI_PHILOSOPHY = 'ai_philosophy'
    CASUAL = 'casual'


class ResponseDepth(str, Enum):
    NONE = 'none'       # pure conversation
    LIGHT = 'light'     # acknowledge + optional one soft insight
    FULL = 'full'       # structured psychology


@dataclass
class IntentResult:
    intent: ConversationIntent
    depth: ResponseDepth
    confidence: float
    reason: str = ''


_GREETING_RE = re.compile(
    r'^(hi|hey|hello|hii|helo|yo|sup|namaste|नमस्ते|नमस्कार|'
    r'good\s*(morning|evening|night)|gm|gn)\b[\s!.?]*$',
    re.I,
)

_SMALL_TALK_RE = re.compile(
    r"(how are you|how r u|kaise ho|kya haal|what'?s up|wyd|"
    r"thanks|thank you|shukriya|bye|goodbye|see you|ok+|okay|cool|nice|hmm+)",
    re.I,
)

_RELATIONSHIP_TERMS = (
    'relationship', 'partner', 'girlfriend', 'boyfriend', 'wife', 'husband',
    'पत्नी', 'पति', 'प्रेमी', 'प्रेमिका', 'रिश्त', 'बातचीत', 'dating',
    'marriage', 'शादी', 'cheat', 'धोख', 'toxic', 'hurt me', 'दुख', 'झगड',
    'breakup', 'ex', 'छोड', 'love', 'pyaar', 'मोहब्बत',
)

_STUDY_TERMS = (
    'study', 'studying', 'padhai', 'पढ़', 'exam', 'focus', 'distract',
    'concentrat', 'career', 'job', 'interview', 'college', 'assignment',
    'procrastinat', 'reels', 'phone', 'scroll', 'brain fog',
)

_LONELINESS_TERMS = (
    'lonely', 'loneliness', 'अकेला', 'अकेल', 'alone', 'कोई नहीं', 'empty',
)

_DEEP_PSYCH_TERMS = (
    'gaslight', 'narcis', 'trauma bond', 'no contact', 'attachment style',
    'dark psych', 'stoic', 'marcus', 'manipul', 'gray rock', 'love bomb',
    'hypergam', 'dopamine', 'amor fati', 'intermittent',
)

_AI_TERMS = (
    'luppi', 'artificial intelligence', 'chatgpt', 'conscious', 'ai companion',
    'digital mind', 'robot',
)


def _word_count(text: str) -> int:
    return len(text.split())


def _is_greeting(text: str) -> bool:
    t = text.strip()
    if len(t) > 40:
        return False
    return bool(_GREETING_RE.match(t))


def _is_small_talk(text: str) -> bool:
    t = text.strip()
    if len(t) > 80:
        return False
    return bool(_SMALL_TALK_RE.search(t))


def _count_hits(text: str, terms: tuple[str, ...]) -> int:
    return sum(1 for t in terms if term_in_text(t, text))


def detect_intent(message: str, memory: SessionMemory | None = None) -> IntentResult:
    text = message.strip()
    lower = text.lower()
    wc = _word_count(lower)

    if not text:
        return IntentResult(ConversationIntent.CASUAL, ResponseDepth.NONE, 0.0, 'empty')

    # ── 1. Greetings & small talk (highest priority) ──
    if _is_greeting(lower):
        return IntentResult(ConversationIntent.GREETING, ResponseDepth.NONE, 1.0, 'greeting_pattern')

    if _is_small_talk(lower) and wc <= 12:
        return IntentResult(ConversationIntent.SMALL_TALK, ResponseDepth.NONE, 0.95, 'small_talk')

    # ── 2. Literal topic intents ──
    rel_hits = _count_hits(lower, _RELATIONSHIP_TERMS)
    study_hits = _count_hits(lower, _STUDY_TERMS)
    lonely_hits = _count_hits(lower, _LONELINESS_TERMS)
    deep_hits = _count_hits(lower, _DEEP_PSYCH_TERMS)
    ai_hits = _count_hits(lower, _AI_TERMS)

    if ai_hits >= 1 and deep_hits == 0 and rel_hits == 0:
        depth = ResponseDepth.FULL if deep_hits or wc > 25 else ResponseDepth.LIGHT
        return IntentResult(ConversationIntent.AI_PHILOSOPHY, depth, 0.85, 'ai_topic')

    if study_hits >= 1 and study_hits >= rel_hits:
        depth = ResponseDepth.LIGHT if wc < 35 or '?' in text else ResponseDepth.FULL
        return IntentResult(ConversationIntent.STUDY_FOCUS, depth, 0.8, 'study_context')

    if rel_hits >= 1:
        depth = ResponseDepth.LIGHT if wc < 30 else ResponseDepth.FULL
        return IntentResult(ConversationIntent.RELATIONSHIP, depth, 0.85, 'relationship_context')

    if lonely_hits >= 1:
        return IntentResult(ConversationIntent.LONELINESS, ResponseDepth.LIGHT, 0.8, 'loneliness')

    if deep_hits >= 2 or (deep_hits >= 1 and wc > 15):
        return IntentResult(ConversationIntent.DEEP_PSYCHOLOGY, ResponseDepth.FULL, 0.9, 'explicit_psych')

    # ── 3. Vague emotional (support, not lecture) ──
    emotional_vague = (
        term_in_text('feel', lower) or term_in_text('feeling', lower) or
        term_in_text('sad', lower) or term_in_text('उदास', lower) or
        term_in_text('stress', lower) or term_in_text('tension', lower) or
        term_in_text('anxious', lower) or term_in_text('overthink', lower)
    )
    if emotional_vague and wc < 25 and deep_hits == 0:
        return IntentResult(ConversationIntent.EMOTIONAL_CHECKIN, ResponseDepth.NONE, 0.75, 'vague_emotion')

    # ── 4. Short casual messages ──
    if wc <= 4 and deep_hits == 0 and rel_hits == 0:
        return IntentResult(ConversationIntent.CASUAL, ResponseDepth.NONE, 0.7, 'short_casual')

    # ── 5. Continuation: user answering LUPPI's question ──
    if memory and memory.turns and wc <= 20:
        last = memory.turns[-1]
        if last.role == 'assistant' and '?' in last.content:
            return IntentResult(ConversationIntent.EMOTIONAL_CHECKIN, ResponseDepth.LIGHT, 0.65, 'follow_up')

    # ── 6. Default: light psychology only if message is substantial ──
    if wc >= 12:
        return IntentResult(ConversationIntent.DEEP_PSYCHOLOGY, ResponseDepth.LIGHT, 0.5, 'default_light')

    return IntentResult(ConversationIntent.CASUAL, ResponseDepth.NONE, 0.6, 'fallback_casual')
