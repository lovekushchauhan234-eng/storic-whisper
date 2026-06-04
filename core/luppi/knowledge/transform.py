from ..domains import Domain
from .types import DomainKnowledge, Insight

TRANSFORM_KNOWLEDGE = DomainKnowledge(
    domain=Domain.TRANSFORM,
    principles=(
        'Identity drives behavior more than willpower speeches.',
        'Self-respect is built in small kept promises.',
        'Transformation is slow architecture, not hype.',
    ),
    insights=(
        Insight(
            'transform_identity_01', Domain.TRANSFORM,
            ('identity', 'खुद', 'बन', 'change', 'नया'),
            '“मैं gym जाता हूँ” vs “मैं वो इंसान हूँ जो body respect करता है” — '
            'different nervous systems।\n\n'
            'Behavior identity के पीछे चलती है। '
            'पहले छोटा proof, फिर story update।',
            weight=1.1,
        ),
        Insight(
            'transform_respect_01', Domain.TRANSFORM,
            ('respect', 'worth', 'value', 'खुद', 'self'),
            'Self-respect speeches से नहीं — kept boundaries से बनती है।\n\n'
            'हर बार जब तुम “हाँ” कहते हो जब “नहीं” feel हो, '
            'तुम खुद को signal भेजते हो: दूसरे ज़रूरी हैं, मैं नहीं।',
        ),
        Insight(
            'transform_habit_01', Domain.TRANSFORM,
            ('habit', 'routine', 'discipline', 'आदत'),
            'Habits moral नहीं — neurological हैं।\n\n'
            'Environment बदलो, cues हटाओ, एक anchor habit रखो। '
            'Motivation का wait मत करो — architecture बनाओ।',
        ),
        Insight(
            'transform_relapse_01', Domain.TRANSFORM,
            ('relapse', 'फिर', 'fail', 'टूट', 'slip'),
            'Slip data है, verdict नहीं।\n\n'
            'Shame loop repeat करती है; curiosity pattern तोड़ती है। '
            'पूछो: trigger क्या था — character नहीं।',
        ),
    ),
)
