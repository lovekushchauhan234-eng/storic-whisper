"""
Family dynamics psychology knowledge for LUPPI 3.0.
"""
from ..domains import Domain
from .types import DomainKnowledge, Insight

FAMILY_KNOWLEDGE = DomainKnowledge(
    domain=Domain.GENERAL,
    principles=(
        'Family patterns often repeat until consciously broken.',
        'Boundaries with family are healthy, not betrayal.',
        'You can love family and still need distance.',
    ),
    insights=(
        Insight(
            'family_patterns_01', Domain.GENERAL,
            ('family', 'parent', 'mother', 'father', 'sibling'),
            'Family dynamics अक्सर unconscious patterns होते हैं।\n\n'
            'जो तुम्हें family में मिला, वो तुम्हारे normal बन जाता है। '
            'Awareness ही इन patterns को break करने का first step है। '
            'You don\'t have to repeat what you inherited।',
            weight=1.1,
        ),
        Insight(
            'family_boundaries_01', Domain.GENERAL,
            ('boundary', 'family', 'parent', 'limit', 'say no'),
            'Boundaries with family betrayal नहीं हैं — self-care हैं।\n\n'
            'Guilt common है पर healthy नहीं। '
            'तुम्हारी mental health family obligations से important है। '
            'Healthy boundaries actually improve relationships long-term में।',
            weight=1.1,
        ),
        Insight(
            'family_distance_01', Domain.GENERAL,
            ('distance', 'cut off', 'no contact', 'family', 'estranged'),
            'Distance from family sometimes necessary होता है।\n\n'
            'यह not loving them का sign नहीं — '
            'protecting yourself का sign है। '
            'Toxic relationships को maintain करना self-harm है।',
            weight=1.15,
        ),
        Insight(
            'family_expectations_01', Domain.GENERAL,
            ('expectation', 'pressure', 'family', 'disappoint', 'let down'),
            'Family expectations heavy हो सकती हैं।\n\n'
            'Disappointing others painful है पर betraying yourself worse है। '
            'तुम्हारी life तुम्हारी है — उनकी projection नहीं। '
            'Their disappointment is about them, not you।',
            weight=1.05,
        ),
    ),
)
