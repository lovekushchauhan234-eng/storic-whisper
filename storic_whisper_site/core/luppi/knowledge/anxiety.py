"""
Anxiety psychology knowledge for LUPPI 3.0.
"""
from ..domains import Domain
from .types import DomainKnowledge, Insight

ANXIETY_KNOWLEDGE = DomainKnowledge(
    domain=Domain.GENERAL,
    principles=(
        'Anxiety is a signal, not a defect.',
        'Control reduces anxiety, but acceptance transforms it.',
        'Anxiety lies about danger.',
    ),
    insights=(
        Insight(
            'anxiety_mechanism_01', Domain.GENERAL,
            ('anxiety', 'worry', 'fear', 'panic', 'anxious'),
            'Anxiety brain का overactive danger detection system है।\n\n'
            'यह false alarms देता है — real danger नहीं। '
            'Understanding यह mechanism ही anxiety को कम करता है '
            'क्योंकि तुम realize करते हो कि यह lie है।',
            weight=1.15,
        ),
        Insight(
            'anxiety_control_01', Domain.GENERAL,
            ('control', 'uncertainty', 'unpredictable', 'worry'),
            'Anxiety control की craving से आती है।\n\n'
            'जितना ज़्यादा तुम control चाहते हो, '
            'उतना ज़्यादा anxiety बढ़ती है। '
            'Acceptance uncertainty की key है — control नहीं।',
            weight=1.1,
        ),
        Insight(
            'anxiety_acceptance_01', Domain.GENERAL,
            ('accept', 'allow', 'resist', 'fight anxiety'),
            'Fighting anxiety उसे बढ़ाता है।\n\n'
            'Allowing anxiety — observing it without judgment — '
            'उसे naturally pass करने देता है। '
            'Resistance prolongs; acceptance releases।',
            weight=1.1,
        ),
        Insight(
            'anxiety_future_01', Domain.GENERAL,
            ('future', 'what if', 'worry about', 'anticipate'),
            'Anxiety mostly future-oriented है — "what if" scenarios।\n\n'
            'Brain worst cases imagine करता है protection के लिए। '
            'यह prediction नहीं, fear है। '
            'Reality अक्सर less scary होती है।',
            weight=1.05,
        ),
        Insight(
            'anxiety_body_01', Domain.GENERAL,
            ('body', 'physical', 'heart', 'breath', 'sweat'),
            'Anxiety mind से शुरू होती है, पर body में feel होती है।\n\n'
            'Heart racing, short breath, tension — ये body की response हैं। '
            'Body को calm करने से mind भी calm होता है। '
            'Breathing से शुरू करो।',
            weight=1.1,
        ),
    ),
)
