"""
LUPPI pipeline — intent first → conversation → optional psychology.
"""
from django.http import HttpRequest

from ..classifier import classify_domain, domain_label
from ..conversational import compose_conversational, intent_to_domain
from ..domains import Domain
from ..emotional import analyze_emotion
from ..engine.composer import compose_reply
from ..engine.response import LuppiResponse
from ..intent import ConversationIntent, ResponseDepth, detect_intent
from ..memory.session import SessionMemoryStore
from ..retrieval import retrieve_insight


def _resolve_domain(intent, message: str) -> Domain:
    suggested = intent_to_domain(intent.intent)
    if suggested:
        return suggested
    if intent.intent == ConversationIntent.RELATIONSHIP:
        lower = message.lower()
        if any(t in lower for t in ('girl', 'women', 'लड़की', 'she', 'her', 'mixed signal')):
            return Domain.WOMEN
        return Domain.BREAKUP
    classification = classify_domain(message)
    if classification.is_strong:
        return classification.domain
    return Domain.GENERAL


def process_message(request: HttpRequest, message: str, provider: str = 'local') -> LuppiResponse:
    message = (message or '').strip()
    if not message:
        return LuppiResponse(
            reply='कुछ लिखो — एक line भी काफी है।',
            domain='general',
            domain_label='Conversation',
            emotion='neutral',
            insight_id=None,
            provider=provider,
            meta={'intent': 'empty'},
        )

    memory_store = SessionMemoryStore(request)
    memory = memory_store.load()
    emotion = analyze_emotion(message)
    intent = detect_intent(message, memory)
    turn_count = len([t for t in memory.turns if t.role == 'user'])

    insight_id = None
    domain = Domain.GENERAL
    retrieval_score = 0.0

    # ── Pure conversation (no psychology dump) ──
    if intent.depth == ResponseDepth.NONE:
        reply = compose_conversational(intent, message, emotion, memory)
        memory_store.append_exchange(
            user_message=message,
            assistant_reply=reply,
            domain='conversation',
            emotion=emotion.primary.value,
            insight_id=None,
        )
        return LuppiResponse(
            reply=reply,
            domain='conversation',
            domain_label='Conversation',
            emotion=emotion.primary.value,
            insight_id=None,
            provider=provider,
            confidence=intent.confidence,
            meta={
                'intent': intent.intent.value,
                'depth': intent.depth.value,
                'reason': intent.reason,
                'session_turns': turn_count + 1,
            },
        )

    # ── Conversational core + optional insight ──
    natural = compose_conversational(intent, message, emotion, memory)
    domain = _resolve_domain(intent, message)

    insight_body = None
    if intent.depth in (ResponseDepth.LIGHT, ResponseDepth.FULL):
        retrieval = retrieve_insight(
            message,
            domain,
            exclude_ids=memory.used_insight_ids[-8:],
        )
        if retrieval and retrieval.is_relevant:
            insight_body = retrieval.insight.body
            insight_id = retrieval.insight.id
            retrieval_score = retrieval.score
            domain = retrieval.insight.domain
        elif intent.depth == ResponseDepth.FULL:
            # Try classifier domain if primary domain had no match
            classification = classify_domain(message)
            if classification.is_strong and classification.domain != domain:
                retrieval = retrieve_insight(
                    message, classification.domain,
                    exclude_ids=memory.used_insight_ids[-8:],
                )
                if retrieval and retrieval.is_relevant:
                    insight_body = retrieval.insight.body
                    insight_id = retrieval.insight.id
                    retrieval_score = retrieval.score
                    domain = retrieval.insight.domain

    # LIGHT mode without relevant insight: stay conversational only
    effective_depth = intent.depth
    if effective_depth == ResponseDepth.LIGHT and not insight_body:
        effective_depth = ResponseDepth.NONE
    if effective_depth == ResponseDepth.FULL and not insight_body:
        effective_depth = ResponseDepth.LIGHT

    reply = compose_reply(
        natural,
        insight_body=insight_body,
        depth=effective_depth,
        emotion=emotion,
        force_ack=bool(insight_body) and emotion.intensity >= 0.5,
    )

    memory_store.append_exchange(
        user_message=message,
        assistant_reply=reply,
        domain=domain.value if isinstance(domain, Domain) else domain,
        emotion=emotion.primary.value,
        insight_id=insight_id,
    )

    return LuppiResponse(
        reply=reply,
        domain=domain.value if isinstance(domain, Domain) else 'conversation',
        domain_label=domain_label(domain) if isinstance(domain, Domain) else 'Conversation',
        emotion=emotion.primary.value,
        insight_id=insight_id,
        provider=provider,
        confidence=intent.confidence,
        meta={
            'intent': intent.intent.value,
            'depth': effective_depth.value,
            'reason': intent.reason,
            'retrieval_score': round(retrieval_score, 3),
            'session_turns': turn_count + 1,
        },
    )
