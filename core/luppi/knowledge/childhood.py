"""
Childhood trauma psychology knowledge for LUPPI 3.0.
"""
from ..domains import Domain
from .types import DomainKnowledge, Insight

CHILDHOOD_KNOWLEDGE = DomainKnowledge(
    domain=Domain.GENERAL,  # Using GENERAL for now, can add new domain later
    principles=(
        'Childhood wounds don\'t define you, but they do shape you.',
        'Healing is possible at any age.',
        'Awareness is the first step to breaking cycles.',
    ),
    insights=(
        Insight(
            'childhood_attachment_01', Domain.GENERAL,
            ('childhood', 'parent', 'child', 'abandon', 'neglect', 'child'),
            'Childhood attachment patterns often repeat in adult relationships।\n\n'
            'जो तुम्हें childhood में मिला था या नहीं मिला, '
            'वो pattern adult relationships में भी दिखता है। '
            'यह awareness ही change का first step है।',
            weight=1.1,
        ),
        Insight(
            'childhood_inner_child_01', Domain.GENERAL,
            ('inner child', 'childhood', 'wound', 'heal', 'inner'),
            'Inner child work यह नहीं कि तुम child बन जाओ — '
            'यह कि तुम अपने child को witness करो और validate करो।\n\n'
            'जो child को तब मिला नहीं था, '
            'adult तुम उसे दे सकते हो।',
            weight=1.1,
        ),
        Insight(
            'childhood_reparenting_01', Domain.GENERAL,
            ('reparent', 'parent yourself', 'self parent', 'nurture'),
            'Reparenting यह है कि तुम खुद को वो दो जो तुम्हें चाहिए था।\n\n'
            'Validation, safety, presence — ये तुम खुद से दे सकते हो। '
            'यह external validation की dependency कम करता है।',
            weight=1.05,
        ),
        Insight(
            'childhood_cycle_breaking_01', Domain.GENERAL,
            ('cycle', 'pattern', 'break', 'repeat', 'generational'),
            'Breaking generational cycles awareness से शुरू होता है।\n\n'
            'जो pattern तुम्हें दिख रहा है, '
            'वो conscious choice बन सकता है unconscious repetition की जगह। '
            'Awareness alone change करती है।',
            weight=1.1,
        ),
    ),
)
