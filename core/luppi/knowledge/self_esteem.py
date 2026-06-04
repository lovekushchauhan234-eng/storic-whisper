"""
Self-esteem psychology knowledge for LUPPI 3.0.
"""
from ..domains import Domain
from .types import DomainKnowledge, Insight

SELF_ESTEEM_KNOWLEDGE = DomainKnowledge(
    domain=Domain.GENERAL,
    principles=(
        'Self-esteem is built through actions, not thoughts.',
        'External validation is temporary; self-validation is permanent.',
        'Self-worth is not earned, it\'s inherent.',
    ),
    insights=(
        Insight(
            'self_esteem_action_01', Domain.GENERAL,
            ('self esteem', 'confidence', 'worth', 'value', 'self worth'),
            'Self-esteem thoughts से नहीं, actions से बनती है।\n\n'
            'जो तुम कहते हो "मैं confident हूँ" वो matter नहीं करता। '
            'जो तुम करते हो — small acts of self-respect — '
            'वो actually build करते हैं।',
            weight=1.1,
        ),
        Insight(
            'self_esteem_external_01', Domain.GENERAL,
            ('approval', 'validation', 'others', 'external', 'people'),
            'External validation temporary relief देती है।\n\n'
            'जब तुम दूसरों से approval माँगते हो, '
            'तुम अपनी power उन्हें दे देते हो। '
            'Self-validation permanent है — वो तुम्हारे पास ही है।',
            weight=1.1,
        ),
        Insight(
            'self_esteem_inherent_01', Domain.GENERAL,
            ('enough', 'worthy', 'deserving', 'inherent'),
            'Self-worth inherent है — earned नहीं।\n\n'
            'तुम्हें prove करने की ज़रूरत नहीं कि तुम enough हो। '
            'यह baseline है — achievement नहीं। '
            'जो खुद को prove करने में लगे हैं, '
            'वो अक्सर खुद को disprove कर रहे होते हैं।',
            weight=1.15,
        ),
        Insight(
            'self_esteem_comparison_01', Domain.GENERAL,
            ('compare', 'better', 'worse', 'others', 'comparison'),
            'Comparison self-esteem का enemy है।\n\n'
            'तुम अपने chapter 5 को उनके chapter 10 से compare कर रहे हो। '
            'Unfair comparison है। '
            'Focus अपनी journey पर — उनके highlight reel पर नहीं।',
            weight=1.05,
        ),
    ),
)
