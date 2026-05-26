"""
Natural conversation layer — human-first responses before psychology depth.
"""
import random

from .domains import Domain
from .emotional import EmotionalContext, EmotionalTone
from .intent import ConversationIntent, IntentResult, ResponseDepth
from .memory.schemas import SessionMemory


def _pick(options: list[str]) -> str:
    return random.choice(options)


GREETING_REPLIES = [
    "Hey 🌙\nHow are you feeling today?",
    "नमस्ते 🌙\nआज कैसा लग रहा है?",
    "Hey — LUPPI here.\nWhat's on your mind?",
]

SMALL_TALK_REPLIES = {
    'how_are_you': [
        "Calm tonight.\nAnd you?",
        "यहाँ शांत हूँ 🌙\nतुम कैसे हो?",
        "Steady.\nतुम्हारा mood कैसा है आज?",
    ],
    'thanks': [
        "🌙",
        "Anytime.",
        "यहाँ हूँ — जब भी चाहो।",
    ],
    'bye': [
        "Take care 🌙",
        "शांति के साथ जाओ।",
    ],
    'default': [
        "🌙",
        "I'm here.",
        "सुन रहा हूँ।",
    ],
}

CASUAL_REPLIES = [
    "सुन रहा हूँ — बताओ थोड़ा और।",
    "I'm listening. What's really on your mind?",
    "यहाँ हूँ। एक line में बताओ — क्या चल रहा है?",
]

EMOTIONAL_CHECKIN_REPLIES = [
    "यह valid है — जो feel हो रहा है, वो real है।\n\nएक line में बताओ: सबसे heavy क्या लग रहा है अभी?",
    "सुन लिया। अभी clarity की ज़रूरत है या बस कोई बिना judge सुने?",
    "Okay. मैं यहाँ हूँ।\n\nथोड़ा context दो — यह feeling कब से है?",
]

STUDY_OPENERS = [
    "पढ़ते समय distraction अक्सर brain की cry होती है — 'मुझे stimulation चाहिए'।",
    "Study mode में mind wander करना failure नहीं — signal है कि task या environment match नहीं कर रहे।",
]

STUDY_FOLLOW_LIGHT = [
    "\n\nएक चीज़ try करो: phone दूसरे room में, सिर्फ 25 minute एक block — बिना perfect होने का pressure।\n\nक्या अभी exam pressure है या general focus?",
]

RELATIONSHIP_OPENERS = [
    "यह सुनकर लगता है कुछ भारी चल रहा है।",
    "Relationship pain अक्सर सिर्फ fight नहीं होता — connection या safety टूटने जैसा feel होता है।",
]

RELATIONSHIP_FOLLOW = [
    "\n\nमैं judge नहीं करूँगा — बस समझना चाहता हूँ।\n\nक्या हाल ही में कोई एक moment है जो सबसे ज़्यादा repeat हो रहा है?",
]

LONELINESS_OPENERS = [
    "अकेलापन कई बार crowd में भी आता है — यह connection की कमी हो सकती है, लोगों की नहीं।",
    "यह feeling valid है। कई बार हम available होते हैं, पर witnessed नहीं feel करते।",
]

LONELINESS_FOLLOW = [
    "\n\nआज रात — क्या तुम्हें किसी specific person की कमी है, या बस खुद से disconnect feel हो रहा है?",
]


def _small_talk_variant(message: str) -> str:
    lower = message.lower()
    if any(x in lower for x in ('how are', 'kaise ho', 'kya haal', "what's up", 'wyd')):
        return _pick(SMALL_TALK_REPLIES['how_are_you'])
    if any(x in lower for x in ('thank', 'shukriya', 'dhanyavad')):
        return _pick(SMALL_TALK_REPLIES['thanks'])
    if any(x in lower for x in ('bye', 'goodbye', 'see you')):
        return _pick(SMALL_TALK_REPLIES['bye'])
    return _pick(SMALL_TALK_REPLIES['default'])


def compose_conversational(
    intent_result: IntentResult,
    message: str,
    emotion: EmotionalContext,
    memory: SessionMemory | None = None,
) -> str:
    intent = intent_result.intent

    if intent == ConversationIntent.GREETING:
        return _pick(GREETING_REPLIES)

    if intent == ConversationIntent.SMALL_TALK:
        return _small_talk_variant(message)

    if intent == ConversationIntent.CASUAL:
        return _pick(CASUAL_REPLIES)

    if intent == ConversationIntent.EMOTIONAL_CHECKIN:
        if memory and memory.turns:
            return (
                "समझा।\n\n"
                "जो बताया — उसके साथ तुम्हारा body और mind दोनों react कर रहे होंगे।\n\n"
                "अगर चाहो, थोड़ा और खोल सकते हो — मैं यहीं हूँ।"
            )
        return _pick(EMOTIONAL_CHECKIN_REPLIES)

    if intent == ConversationIntent.STUDY_FOCUS:
        base = _pick(STUDY_OPENERS)
        if intent_result.depth == ResponseDepth.LIGHT:
            return base + _pick(STUDY_FOLLOW_LIGHT)
        return base + _pick(STUDY_FOLLOW_LIGHT)

    if intent == ConversationIntent.RELATIONSHIP:
        parts = [_pick(RELATIONSHIP_OPENERS)]
        if emotion.primary in (EmotionalTone.GRIEF, EmotionalTone.ATTACHMENT, EmotionalTone.CONFUSION):
            parts[0] = "यह भारी लग रहा है — और यह valid है।"
        return parts[0] + _pick(RELATIONSHIP_FOLLOW)

    if intent == ConversationIntent.LONELINESS:
        return _pick(LONELINESS_OPENERS) + _pick(LONELINESS_FOLLOW)

    if intent == ConversationIntent.AI_PHILOSOPHY:
        if intent_result.depth == ResponseDepth.NONE:
            return "मैं LUPPI हूँ 🌙\nPsychology companion — casual बात भी, depth भी।\n\nतुम क्या जानना चाहते हो?"
        return (
            "AI और mind के बीच सवाल अक्सर tech नहीं — attachment का होता है।\n\n"
            "तुम्हें क्या feel होता है जब तुम यहाँ बात करते हो — comfort, curiosity, या कुछ और?"
        )

    return _pick(CASUAL_REPLIES)


def intent_to_domain(intent: ConversationIntent) -> Domain | None:
    """Suggested domain when depth allows — not used for greetings."""
    mapping = {
        ConversationIntent.STUDY_FOCUS: Domain.DOPAMINE,
        ConversationIntent.RELATIONSHIP: Domain.BREAKUP,
        ConversationIntent.LONELINESS: Domain.HUMAN,
        ConversationIntent.AI_PHILOSOPHY: Domain.AIMIND,
        ConversationIntent.DEEP_PSYCHOLOGY: None,
    }
    return mapping.get(intent)


def trim_insight_for_light(insight_body: str, max_sentences: int = 2) -> str:
    """One soft insight paragraph — not a lecture."""
    parts = insight_body.replace('\n\n', '\n').split('\n')
    text = ' '.join(p.strip() for p in parts if p.strip())
    sentences = []
    buf = ''
    for char in text:
        buf += char
        if char in '.!?|' and len(buf.strip()) > 20:
            sentences.append(buf.strip())
            buf = ''
        if len(sentences) >= max_sentences:
            break
    if not sentences and buf.strip():
        sentences.append(buf.strip()[:280])
    return '\n\n'.join(sentences[:max_sentences])
