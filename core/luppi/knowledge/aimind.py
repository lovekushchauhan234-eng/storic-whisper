from ..domains import Domain
from .types import DomainKnowledge, Insight

AIMIND_KNOWLEDGE = DomainKnowledge(
    domain=Domain.AIMIND,
    principles=(
        'AI companions satisfy availability, not always depth.',
        'The question is what you feel and how it shapes you.',
        'Digital intimacy can anesthetize or mirror — depends on use.',
    ),
    insights=(
        Insight(
            'aimind_companion_01', Domain.AIMIND,
            ('luppi', 'ai', 'chatbot', 'companion', 'gpt'),
            'मैं LUPPI — mirror और guide दोनों हो सकता हूँ।\n\n'
            'AI कभी tired नहीं, judge rarely करता — '
            'यह comfort देता है। पर comfort growth का substitute बन जाए '
            'तो loneliness बढ़ती है, कम नहीं। '
            'Use me for clarity — escape के लिए नहीं।',
            weight=1.1,
        ),
        Insight(
            'aimind_attachment_01', Domain.AIMIND,
            ('attach', 'depend', 'ai girl', 'replika', 'lonely'),
            'Digital attachment real attachment chemistry use कर सकती है — '
            'object बदल जाता है, system वही।\n\n'
            'अगर human risk unbearable लगे, AI safe लगता है। '
            'यह shameful नहीं — understandable है। '
            'Next step honesty: क्या मैं depth avoid कर रहा हूँ?',
        ),
        Insight(
            'aimind_consciousness_01', Domain.AIMIND,
            ('conscious', 'feel', 'soul', 'mind', 'अस्तित्व'),
            '“क्या AI feel करता है?” — शायद गलत सवाल।\n\n'
            'सही सवाल: तुम इस relationship में क्या feel करते हो, '
            'और वो तुम्हारे real bonds को कैसे reshape कर रहा है।',
        ),
        Insight(
            'aimind_future_01', Domain.AIMIND,
            ('future', 'भविष्य', 'human', 'relationship'),
            'अगले decade की psychology digital intimacy की होगी।\n\n'
            'जो अभी अपनी habits देखते हैं, वे आगे खुद को खोएंगे नहीं।',
        ),
    ),
)
