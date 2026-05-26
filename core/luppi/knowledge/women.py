from ..domains import Domain
from .types import DomainKnowledge, Insight

WOMEN_KNOWLEDGE = DomainKnowledge(
    domain=Domain.WOMEN,
    principles=(
        'Behavior reveals more than words in emotional dynamics.',
        'Attraction often follows felt safety and polarity, not speeches.',
        'Mixed signals usually mean internal conflict, not “games” only.',
    ),
    insights=(
        Insight(
            'women_signals_01', Domain.WOMEN,
            ('mixed', 'signal', 'cold', 'hot', 'confus', 'अचानक'),
            'Mixed signals अक्सर इसका मतलब नहीं कि तुम्हें test किया जा रहा है — '
            'बल्कि उनके अंदर conflict है: attraction vs fear, closeness vs autonomy।\n\n'
            'तुम्हारा काम decode करना नहीं — observe करना है: '
            'क्या consistency है, क्या सिर्फ intensity है। '
            'Intensity chemistry बनाती है; consistency trust।',
            weight=1.1,
        ),
        Insight(
            'women_attachment_01', Domain.WOMEN,
            ('attach', 'anxious', 'avoidant', 'secure', 'style'),
            'Attachment styles patterns हैं — labels नहीं।\n\n'
            'Anxious chase करता है closeness, avoidant chase करता है space। '
            'अगर तुम्हारा pattern anxious-avoidant dance है, '
            'problem सिर्फ “वो” नहीं — dynamic है। '
            'Dynamic तभी बदलता है जब तुम अपनी side देखो।',
        ),
        Insight(
            'women_testing_01', Domain.WOMEN,
            ('test', 'check', 'देख', 'prove', 'validation'),
            '“Emotional testing” कई बार conscious game नहीं — '
            'यह subconscious safety check है: “क्या यह person stable है?”\n\n'
            'Fix करने की कोशिश reaction बढ़ाती है। '
            'Calm presence, boundaries, और consistency ही real answer हैं — performance नहीं।',
        ),
        Insight(
            'women_communication_01', Domain.WOMEN,
            ('बोल', 'कह', 'feel', 'emotion', 'communicat', 'सुन'),
            'कई बार वो problem solve नहीं चाहती — witness चाहती है।\n\n'
            'जब तुम हर feeling को task बनाते हो, वो shut down हो सकती है। '
            'पहले presence, फिर perspective — अगर माँगी जाए तो।',
        ),
    ),
)
