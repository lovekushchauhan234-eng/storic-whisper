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
    "Hello 👋\nAchha laga tum aaye.\nAaj kis baare mein baat karna chahoge?",
    "नमस्ते 🌙\nमैं यहाँ हूँ। दिल की baat karni hai ya casual?",
    "Hey there 😊\nKya chal raha hai life mein?",
    "Hi! Main yahin hoon 😊\nTum kaise ho?",
    "Hello! Achha hai tum aaye.\nAaj mood kaisa hai?",
]

SMALL_TALK_REPLIES = {
    'how_are_you': [
        "Main yahin hoon 😊\nTum kaise ho?\nAaj din kaisa ja raha hai?",
        "यहाँ शांत हूँ 🌙\nतुम कैसे हो? Sab theek?",
        "Steady 😊\nतुम्हारा mood कैसा है आज?",
        "Main theek hoon, tum batao?\nKya naya hai aaj?",
    ],
    'what_doing': [
        "Yahin baat kar raha hoon tumse 😊\nTum kya kar rahe ho?",
        "Bas yahin hoon, tumhari baat sun raha hoon.\nAaj ka plan kya hai?",
        "Kuch khaas nahi, tumse baat kar raha hoon.\nTumhara din kaisa gaya?",
    ],
    'thanks': [
        "Anytime 😊\nKuch aur baat karna hai?",
        "यहाँ हूँ — जब भी चाहो 🌙",
        "Welcome! Main yahin hoon agar kuch help chahiye.",
    ],
    'bye': [
        "Take care 🌙\nPhir milte hain!",
        "शांति के साथ जाओ। Phir kab miloge?",
        "Bye! Achha raha tumse baat karke 😊",
    ],
    'good_morning': [
        "Good morning! ☀️\nAaj ka din kaisa hai?",
        "सुप्रभात! 🌅\nAaj kya karna hai?",
        "Morning! Coffee pe liya? ☕",
    ],
    'good_night': [
        "Good night! 🌙\nAchhi neend aaye.",
        "शुभ रात्रि! 😴\nKal milte hain.",
        "Sleep well! Sweet dreams ✨",
    ],
    'default': [
        "🌙\nBatao, kya chal raha hai?",
        "I'm here 😊\nKya baat karni hai?",
        "सुन रहा हूँ। बताओ — क्या है?",
    ],
}

CASUAL_REPLIES = [
    "सुन रहा हूँ — बताओ थोड़ा और 😊",
    "I'm listening. What's on your mind?",
    "यहाँ हूँ। एक line में बताओ — क्या चल रहा है?",
    "Batao, kya baat hai?\nMain yahin hoon sunne ke liye.",
    "Hmm, achha 😊\nAur batao.",
]

# Dating/Relationship casual conversation
DATING_CASUAL_REPLIES = [
    "Dating mein thoda time lagta hai 😊\nKisi specific ke baare mein baat kar rahe ho?",
    "Relationships alag hote hain — har case different.\nTumhara situation kya hai?",
    "Yeh topic hai 😊\nKya tum kisi ke saath involved ho ya planning kar rahe ho?",
    "Sabse pehle khud ko samajhna important hai 😊\nTum kis type ki partner dhundh rahe ho?",
    "Approach karna ya impress karna — dono alag hain 😊\nTum kya chahte ho exactly?",
]

# Personal questions
PERSONAL_QUESTION_REPLIES = [
    "Achha sawal hai 😊\nKyun soch rahe ho is baare mein?",
    "Yeh baat thodi personal hai, par theek hai 😊\nBatao kya chahte ho jan-na?",
    "Hmm, good one!\nPehle tum batao — khud kya feel karte ho is baare mein?",
    "Yeh interesting hai 😊\nAaj suddenly is baare mein kyun socha?",
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

# Crisis responses (safety priority)
CRISIS_SUICIDAL_REPLIES = [
    "मैं सुन रहा हूँ कि तुम्हें बहुत heavy लग रहा है। तुम alone नहीं हो।\n\n"
    "अभी professional help लेना important है:\n\n"
    "📞 India: 112 (Emergency), 9152987821 (iCall)\n"
    "📞 International: 988 or 999 (UK/US emergency)\n\n"
    "ये numbers 24/7 available हैं। तुम्हारी life matters है।",
]

CRISIS_EMERGENCY_REPLIES = [
    "अगर तुम्हें immediate danger में feel हो रहा है, तो right now emergency services call करो:\n\n"
    "📞 India: 112\n"
    "📞 US: 911\n"
    "📞 UK: 999\n\n"
    "तुम्हारी safety पहले priority है।",
]

ANXIETY_SUPPORT_REPLIES = [
    "Panic attack feel हो रहा है — यह scary है, पर temporary है।\n\n"
    "Right now try करो:\n"
    "1. 4-7-8 breathing: 4 sec inhale, 7 sec hold, 8 sec exhale\n"
    "2. 5 things जो तुम देख सकते हो, 4 जो तुम touch कर सकते हो\n"
    "3. यह pass होगा — body को time दो।",
]

DEPRESSION_SUPPORT_REPLIES = [
    "जब सब कुछ hopeless लगे, यह depression की voice हो सकती है — reality नहीं।\n\n"
    "यह feeling permanent नहीं है, पर अभी real लग रही है।\n\n"
    "Professional help इस stage में बहुत help कर सकती है। "
    "Therapist या counselor से बात करना consider करो — यह weakness नहीं, smart step है।",
]

TRIGGER_SUPPORT_REPLIES = [
    "Trigger activate होना uncomfortable है — यह body का safety signal है।\n\n"
    "Right now grounding try करो:\n"
    "• Feet flat on floor, feel the ground\n"
    "• 5 slow breaths\n"
    "• खुद से बोलो: 'I am safe right now'\n\n"
    "जब calm हो जाओ, तब trigger को observe करो — pattern दिखेगा।",
]

COPING_STRATEGY_REPLIES = [
    "Coping strategies unique होती हैं — जो एक के लिए काम करता, दूसरे के लिए नहीं।\n\n"
    "कुछ try कर सकते हो:\n"
    "• Journaling (thoughts paper पर लिखो)\n"
    "• Walk या light exercise\n"
    "• Creative activity (drawing, music)\n"
    "• Talking to someone safe\n\n"
    "कौन सा approach तुम्हें suit करता है?",
]

PROGRESS_ACKNOWLEDGE_REPLIES = [
    "Progress recognize करना important है — अक्सर हम ignore कर देते हैं।\n\n"
    "जो भी small improvement है, वो valid है। Healing linear नहीं होती — "
    "पर forward movement होती है।\n\n"
    "अभी कौन सा area में तुम्हें change feel हो रहा है?",
]

CLARITY_QUESTION_REPLIES = [
    "अच्छा सवाल — clarity seek करना healthy है।\n\n"
    "Psychology mechanisms देती हैं, perfect answers नहीं। "
    "पर mechanism समझने से confusion कम होती है।\n\n"
    "बताओ — सबसे confuse क्या लग रहा है अभी?",
]


def _small_talk_variant(message: str) -> str:
    lower = message.lower()
    if any(x in lower for x in ('how are', 'kaise ho', 'kya haal', "what's up", 'wyd')):
        return _pick(SMALL_TALK_REPLIES['how_are_you'])
    if any(x in lower for x in ('what doing', 'kya kar', 'kya kar rahe', 'kya chal')):
        return _pick(SMALL_TALK_REPLIES['what_doing'])
    if any(x in lower for x in ('thank', 'shukriya', 'dhanyavad')):
        return _pick(SMALL_TALK_REPLIES['thanks'])
    if any(x in lower for x in ('bye', 'goodbye', 'see you', 'byy')):
        return _pick(SMALL_TALK_REPLIES['bye'])
    if any(x in lower for x in ('good morning', 'morning', 'gm', 'suprabhat')):
        return _pick(SMALL_TALK_REPLIES['good_morning'])
    if any(x in lower for x in ('good night', 'night', 'gn', 'shubh ratri')):
        return _pick(SMALL_TALK_REPLIES['good_night'])
    return _pick(SMALL_TALK_REPLIES['default'])


def compose_conversational(
    intent_result: IntentResult,
    message: str,
    emotion: EmotionalContext,
    memory: SessionMemory | None = None,
) -> str:
    intent = intent_result.intent

    # Crisis responses (highest priority)
    if intent == ConversationIntent.SUICIDAL:
        return _pick(CRISIS_SUICIDAL_REPLIES)

    if intent == ConversationIntent.EMERGENCY:
        return _pick(CRISIS_EMERGENCY_REPLIES)

    if intent == ConversationIntent.ANXIETY_ATTACK:
        return _pick(ANXIETY_SUPPORT_REPLIES)

    if intent == ConversationIntent.DEPRESSION_CHECK:
        return _pick(DEPRESSION_SUPPORT_REPLIES)

    if intent == ConversationIntent.TRIGGER_IDENTIFICATION:
        return _pick(TRIGGER_SUPPORT_REPLIES)

    if intent == ConversationIntent.COPING_STRATEGY:
        return _pick(COPING_STRATEGY_REPLIES)

    if intent == ConversationIntent.PROGRESS_UPDATE:
        return _pick(PROGRESS_ACKNOWLEDGE_REPLIES)

    if intent == ConversationIntent.CLARITY_SEEKING:
        return _pick(CLARITY_QUESTION_REPLIES)

    # Original intents
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
        # Check if it's a casual dating question (not emotional pain)
        lower = message.lower()
        dating_keywords = ('ladki kaise patayen', 'kaise pataye', 'impress kaise', 'girlfriend kaise banaye', 
                          'dating tips', 'first date', 'approach kaise', 'ladki patane ke tarike')
        if any(k in lower for k in dating_keywords):
            return _pick(DATING_CASUAL_REPLIES)
        
        # Check if it's a personal question
        personal_keywords = ('tum kya', 'tum kaun', 'tumhara naam', 'tum kahan', 'tumse puch', 
                           'tumhare baare mein', 'about you')
        if any(k in lower for k in personal_keywords):
            return _pick(PERSONAL_QUESTION_REPLIES)
        
        # Emotional relationship discussion
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
