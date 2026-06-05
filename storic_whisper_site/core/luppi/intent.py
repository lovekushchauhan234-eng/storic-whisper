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
    # Crisis intents (safety priority)
    SUICIDAL = 'suicidal'
    SELF_HARM = 'self_harm'
    EMERGENCY = 'emergency'
    # Enhanced intents
    ANXIETY_ATTACK = 'anxiety_attack'
    DEPRESSION_CHECK = 'depression_check'
    TRIGGER_IDENTIFICATION = 'trigger_identification'
    COPING_STRATEGY = 'coping_strategy'
    PROGRESS_UPDATE = 'progress_update'
    CLARITY_SEEKING = 'clarity_seeking'


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

# Simple affirmations (I'm fine, okay, etc.)
_SIMPLE_AFFIRMATION_RE = re.compile(
    r'^(main|mein|i\'?m|i am)\s+(theek|thik|fine|okay|ok|good|accha)\b',
    re.I,
)

_SMALL_TALK_RE = re.compile(
    r"(how are you|how r u|kaise ho|kya haal|what'?s up|wyd|"
    r"thanks|thank you|shukriya|bye|goodbye|see you|ok+|okay|cool|nice|hmm+|"
    r"what doing|kya kar|kya kar rahe|kya chal|good morning|good night)",
    re.I,
)

_RELATIONSHIP_TERMS = (
    'relationship', 'partner', 'girlfriend', 'boyfriend', 'wife', 'husband',
    'पत्नी', 'पति', 'प्रेमी', 'प्रेमिका', 'रिश्त', 'बातचीत', 'dating',
    'marriage', 'शादी', 'cheat', 'धोख', 'toxic', 'hurt me', 'दुख', 'झगड',
    'breakup', 'ex', 'छोड', 'love', 'pyaar', 'मोहब्बत',
    # Dating/casual terms
    'ladki', 'girl', 'pataye', 'impress', 'approach', 'date', 'crush',
    'पटाने', 'इम्प्रेस', 'लड़की', 'प्रपोज़',
    # Getting someone back terms
    'vapas', 'वापस', 'wapas', 'laye', 'laaye', 'le', 'wapis', 'वापिस',
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

_CRISIS_TERMS = (
    'suicide', 'kill myself', 'want to die', 'end it all', 'suicidal',
    'आत्महत्या', 'मरना', 'जीवन खत्म', 'end my life',
)

_SELF_HARM_TERMS = (
    'cut', 'hurt myself', 'self harm', 'self-harm', 'injure',
    'खुद को चोट', 'आत्महत्या करना',
)

_EMERGENCY_TERMS = (
    'emergency', 'help now', 'urgent', '911', 'police',
    'immediate danger', 'आपातकाल',
)

_ANXIETY_TERMS = (
    'panic attack', 'anxiety attack', 'cant breathe', 'heart racing',
    'hyperventilating', 'panic', 'घबराहट',
)

_DEPRESSION_TERMS = (
    'depressed', 'depression', 'hopeless', 'worthless', 'nothing matters',
    'उदास', 'निराश', 'बेकार',
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

    # ── 0. CRISIS DETECTION (highest priority - safety first) ──
    crisis_hits = _count_hits(lower, _CRISIS_TERMS)
    self_harm_hits = _count_hits(lower, _SELF_HARM_TERMS)
    emergency_hits = _count_hits(lower, _EMERGENCY_TERMS)

    if crisis_hits >= 1 or self_harm_hits >= 1:
        return IntentResult(ConversationIntent.SUICIDAL, ResponseDepth.NONE, 1.0, 'crisis_detected')

    if emergency_hits >= 1:
        return IntentResult(ConversationIntent.EMERGENCY, ResponseDepth.NONE, 1.0, 'emergency_detected')

    # ── 1. Greetings & small talk ──
    if _is_greeting(lower):
        return IntentResult(ConversationIntent.GREETING, ResponseDepth.NONE, 1.0, 'greeting_pattern')

    # Simple affirmations (I'm fine, etc.) - treat as casual, not deep topic
    if _SIMPLE_AFFIRMATION_RE.match(lower):
        return IntentResult(ConversationIntent.CASUAL, ResponseDepth.NONE, 0.95, 'simple_affirmation')

    if _is_small_talk(lower) and wc <= 15:
        return IntentResult(ConversationIntent.SMALL_TALK, ResponseDepth.NONE, 0.95, 'small_talk')

    # ── 2. Anxiety & depression detection ──
    anxiety_hits = _count_hits(lower, _ANXIETY_TERMS)
    depression_hits = _count_hits(lower, _DEPRESSION_TERMS)

    if anxiety_hits >= 1:
        return IntentResult(ConversationIntent.ANXIETY_ATTACK, ResponseDepth.LIGHT, 0.9, 'anxiety_detected')

    if depression_hits >= 2:
        return IntentResult(ConversationIntent.DEPRESSION_CHECK, ResponseDepth.LIGHT, 0.85, 'depression_detected')

    # ── 3. Literal topic intents ──
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

    # ── 4. Enhanced intent detection ──
    if '?' in text and wc >= 5:
        return IntentResult(ConversationIntent.CLARITY_SEEKING, ResponseDepth.LIGHT, 0.75, 'question_asked')

    if any(t in lower for t in ('trigger', 'remind', 'flashback', 'memory')):
        return IntentResult(ConversationIntent.TRIGGER_IDENTIFICATION, ResponseDepth.LIGHT, 0.8, 'trigger_mentioned')

    if any(t in lower for t in ('cope', 'handle', 'deal', 'manage')):
        return IntentResult(ConversationIntent.COPING_STRATEGY, ResponseDepth.LIGHT, 0.75, 'coping_requested')

    if any(t in lower for t in ('better', 'improve', 'progress', 'healing')):
        return IntentResult(ConversationIntent.PROGRESS_UPDATE, ResponseDepth.LIGHT, 0.7, 'progress_mentioned')

    # ── 5. Vague emotional (support, not lecture) ──
    emotional_vague = (
        term_in_text('feel', lower) or term_in_text('feeling', lower) or
        term_in_text('sad', lower) or term_in_text('उदास', lower) or
        term_in_text('stress', lower) or term_in_text('tension', lower) or
        term_in_text('anxious', lower) or term_in_text('overthink', lower)
    )
    
    # Hindi emotional pain indicators
    emotional_pain_hindi = (
        term_in_text('tut', lower) or term_in_text('टूट', lower) or
        term_in_text('dard', lower) or term_in_text('दर्द', lower) or
        term_in_text('rona', lower) or term_in_text('रोना', lower) or
        term_in_text('bilkul', lower) or term_in_text('बिल्कुल', lower)
    )
    
    if emotional_pain_hindi and wc < 20 and deep_hits == 0:
        return IntentResult(ConversationIntent.EMOTIONAL_CHECKIN, ResponseDepth.NONE, 0.85, 'emotional_pain_hindi')
    
    if emotional_vague and wc < 25 and deep_hits == 0:
        return IntentResult(ConversationIntent.EMOTIONAL_CHECKIN, ResponseDepth.NONE, 0.75, 'vague_emotion')

    # ── 6. Short casual messages ──
    if wc <= 6 and deep_hits == 0 and rel_hits == 0:
        return IntentResult(ConversationIntent.CASUAL, ResponseDepth.NONE, 0.7, 'short_casual')

    # ── 7. Continuation: user answering LUPPI's question ──
    if memory and memory.turns and wc <= 20:
        last = memory.turns[-1]
        if last.role == 'assistant' and '?' in last.content:
            # Check if it's a simple affirmation (not emotional)
            if not _SIMPLE_AFFIRMATION_RE.match(lower):
                return IntentResult(ConversationIntent.EMOTIONAL_CHECKIN, ResponseDepth.LIGHT, 0.65, 'follow_up')
            else:
                return IntentResult(ConversationIntent.CASUAL, ResponseDepth.NONE, 0.7, 'follow_up_casual')

    # ── 8. Default: light psychology only if message is substantial ──
    # But NOT if it's a simple question about getting someone back (relationship)
    relationship_question = (
        term_in_text('vapas', lower) or term_in_text('वापस', lower) or
        term_in_text('wapas', lower) or term_in_text('kaise', lower) and 
        (term_in_text('laye', lower) or term_in_text('laaye', lower) or term_in_text('le', lower))
    )
    
    if relationship_question and rel_hits >= 1:
        return IntentResult(ConversationIntent.RELATIONSHIP, ResponseDepth.LIGHT, 0.8, 'relationship_question')
    
    if wc >= 12:
        return IntentResult(ConversationIntent.DEEP_PSYCHOLOGY, ResponseDepth.LIGHT, 0.5, 'default_light')

    return IntentResult(ConversationIntent.CASUAL, ResponseDepth.NONE, 0.6, 'fallback_casual')
