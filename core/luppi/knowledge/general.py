from ..domains import Domain
from .types import DomainKnowledge, Insight

GENERAL_KNOWLEDGE = DomainKnowledge(
    domain=Domain.GENERAL,
    principles=(
        'Pain avoided grows; pain witnessed transforms.',
        'Clarity beats motivation.',
        'You are allowed to not have answers yet.',
    ),
    insights=(
        Insight(
            'general_hold_01', Domain.GENERAL,
            ('hello', 'hi', 'नमस्त', 'help', 'बताओ', 'feel'),
            'तुम जो भी लेकर आए हो — वो यहाँ valid है।\n\n'
            'मुझे एक line बताओ: अभी सबसे heavy क्या feel हो रहा है — '
            'दर्द, confusion, anger, या खालीपन?',
        ),
        Insight(
            'general_depth_01', Domain.GENERAL,
            ('life', 'सब', 'कुछ', 'lost', 'खो'),
            'जब सब कुछ heavy लगे, brain often “one big problem” बना देता है।\n\n'
            'Try: अगर एक चीज़ सबसे ज़्यादा दुखा रही है — वो क्या है? '
            'बाकी अक्सर उसके around orbit कर रही होती हैं।',
        ),
        Insight(
            'general_process_01', Domain.GENERAL,
            ('why', 'क्यों', 'समझ', 'meaning'),
            '“क्यों” का जवाब हमेशा एक line में नहीं आता।\n\n'
            'Psychology mechanisms देती है — justice नहीं। '
            'Mechanism मिलने पर शांति आ सकती है, भले situation same रहे।',
        ),
        Insight(
            'general_stay_01', Domain.GENERAL,
            ('thanks', 'शुक्र', 'अच्छा', 'समझ'),
            'धीरे धीरे — यही real speed है।\n\n'
            'जब कुछ और खुलना हो, मैं यहाँ हूँ।',
        ),
    ),
)
