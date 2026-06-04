from ..domains import Domain
from .types import DomainKnowledge, Insight

DOPAMINE_KNOWLEDGE = DomainKnowledge(
    domain=Domain.DOPAMINE,
    principles=(
        'Dopamine signals anticipation more than pleasure.',
        'Cheap stimulation raises baseline and kills depth.',
        'Boredom tolerance is a trainable capacity.',
    ),
    insights=(
        Insight(
            'dopamine_anticipation_01', Domain.DOPAMINE,
            ('dopamine', 'reel', 'scroll', 'phone', 'addict', 'instagram'),
            'Feeds खतरनाक इसलिए नहीं कि content बुरा है — '
            'क्योंकि reward unpredictable है। Variable rewards सबसे strong loop बनाते हैं।\n\n'
            'तुम content consume नहीं कर रहे — तुम uncertainty chase कर रहे हो।',
            weight=1.15,
        ),
        Insight(
            'dopamine_porn_01', Domain.DOPAMINE,
            ('porn', 'masturb', 'आसक्त', 'urge'),
            'Porn loop अक्सर intimacy की जगह instant relief है — shame के साथ।\n\n'
            'यह moral failure नहीं — hijacked anticipation system है। '
            'Recovery shame से नहीं — friction, boredom tolerance और real connection से शुरू होती है।',
        ),
        Insight(
            'dopamine_baseline_01', Domain.DOPAMINE,
            ('bored', 'fog', 'focus', 'motivation', 'ऊब'),
            'जब हर घंटे high stimulation मिलती है, normal life flat लगती है।\n\n'
            'Books slow, people boring, silence uncomfortable — '
            'यह personality नहीं, rewired baseline है। '
            'Reset boring hours को वापस लाता है।',
        ),
        Insight(
            'dopamine_attention_01', Domain.DOPAMINE,
            ('attention', 'focus', 'scatter', 'multitask'),
            'Attention fragmented है तो identity fragmented feel होती है।\n\n'
            'Deep work एक luxury नहीं — nervous system की rehab है।',
        ),
    ),
)
