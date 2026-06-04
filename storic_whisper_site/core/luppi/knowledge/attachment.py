"""
Attachment Theory knowledge for LUPPI 3.0.
"""
from ..domains import Domain
from .types import DomainKnowledge, Insight


ATTACHMENT_KNOWLEDGE = DomainKnowledge(
    domain=Domain.BREAKUP,
    principles=(
        "Attachment styles form in childhood but can change in adulthood",
        "Secure attachment is the foundation for healthy relationships",
        "Anxious and avoidant patterns are adaptive responses to early experiences",
        "Understanding your attachment style is the first step to change",
        "Attachment wounds can heal through secure relationships and therapy",
    ),
    insights=(
        Insight(
            'attachment_1', Domain.BREAKUP,
            ('attach', 'anxious', 'avoidant', 'childhood', 'abandonment', 'insecure'),
            "Anxious attachment develops when caregivers were inconsistent - sometimes available, sometimes not. This creates a deep fear of abandonment and a constant need for reassurance. In adult relationships, this shows up as: excessive worry about the partner's feelings, difficulty being alone, constant seeking of validation, and interpreting neutral actions as rejection. The pattern isn't a flaw - it's an adaptation to inconsistent early care. Healing involves: learning to self-soothe, building internal security, recognizing that past inconsistency doesn't mean current relationships will be the same, and gradually testing secure relationships.",
        ),
        Insight(
            'attachment_2', Domain.BREAKUP,
            ('avoidant', 'withdraw', 'intimacy', 'cold', 'distance', 'independent'),
            "Avoidant attachment develops when caregivers were emotionally unavailable or rejecting. This teaches that needs won't be met, so it's safer to not have them. In adult relationships, this shows up as: difficulty with intimacy, valuing independence over connection, withdrawing when conflict arises, and feeling suffocated by emotional closeness. The withdrawal isn't coldness - it's a learned protection. Healing involves: recognizing that needs are valid, learning to tolerate vulnerability, understanding that closeness doesn't mean engulfment, and practicing gradual emotional sharing.",
        ),
        Insight(
            'attachment_3', Domain.BREAKUP,
            ('secure', 'trust', 'healthy', 'consistent', 'available'),
            "Secure attachment develops when caregivers were consistently responsive and emotionally available. This creates an internal template that: relationships can be trusted, needs will be met, it's safe to be vulnerable, and conflict can be resolved. Even if you didn't have this foundation, you can develop it through: consistent secure relationships (friends, partners, therapists), practicing self-compassion, learning to recognize safe vs unsafe dynamics, and gradually testing vulnerability in appropriate contexts. Secure attachment isn't about never feeling anxious - it's about having the capacity to recover from distress.",
        ),
        Insight(
            'attachment_4', Domain.BREAKUP,
            ('pattern', 'cycle', 'anxious', 'avoidant', 'dynamic', 'relationship'),
            "Adult relationships often recreate early attachment patterns. Anxious + avoidant is a common but challenging dynamic - the anxious partner seeks closeness, the avoidant partner withdraws, creating a cycle. Secure + anxious can work if the secure partner provides consistency. Secure + avoidant can work if the avoidant partner learns to tolerate closeness. The key insight: you can't change your partner's attachment style, but you can change how you respond. Focus on: your own patterns, what you need from relationships, whether your current relationship can provide that, and building security independently of your partner.",
        ),
        Insight(
            'attachment_5', Domain.BREAKUP,
            ('heal', 'wound', 'therapy', 'recovery', 'corrective', 'experience'),
            "Attachment wounds heal through corrective emotional experiences - relationships that are different from early ones. This can happen with: a therapist who is consistently present, friends who show up reliably, partners who demonstrate security over time. The healing process involves: recognizing the wound (not just the symptom), grieving the early experience you didn't have, learning to self-regulate when triggered, and gradually testing new relationship patterns. It's not about forgetting the past - it's about integrating it so it doesn't control your present. Healing is possible at any age, but it requires consistent safe experiences.",
        ),
    ),
)
