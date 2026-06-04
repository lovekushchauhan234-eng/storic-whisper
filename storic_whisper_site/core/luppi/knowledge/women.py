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
from ..domains import Domain
from .types import DomainKnowledge, Insight

WOMEN_KNOWLEDGE = DomainKnowledge(
    domain=Domain.WOMEN,
    principles=(
        'Behavior reveals more than words in emotional dynamics.',
        'Attraction follows felt safety and polarity, not speeches.',
        'Mixed signals usually mean internal conflict, not games.',
        'Presence and consistency beat performance.',
        'Emotional validation precedes logical connection.',
    ),
    insights=(
        Insight(
            'women_signals_01', Domain.WOMEN,
            ('mixed', 'signal', 'cold', 'hot', 'confus', 'अचानक', 'ignore', 'reply', 'seen'),
            'Mixed signals अक्सर इसका मतलब नहीं कि तुम्हें test किया जा रहा है — '
            'बल्कि उनके अंदर conflict है: attraction vs fear, closeness vs autonomy।\n\n'
            'तुम्हारा काम decode करना नहीं — observe करना है: '
            'क्या consistency है, क्या सिर्फ intensity है। '
            'Intensity chemistry बनाती है; consistency trust।',
            weight=1.1,
        ),
        Insight(
            'women_attachment_01', Domain.WOMEN,
            ('attach', 'anxious', 'avoidant', 'secure', 'style', 'clingy', 'possessive'),
            'Attachment styles patterns हैं — labels नहीं।\n\n'
            'Anxious chase करता है closeness, avoidant chase करता है space। '
            'अगर तुम्हारा pattern anxious-avoidant dance है, '
            'problem सिर्फ "वो" नहीं — dynamic है। '
            'Dynamic तभी बदलता है जब तुम अपनी side देखो।',
        ),
        Insight(
            'women_testing_01', Domain.WOMEN,
            ('test', 'check', 'देख', 'prove', 'validation', 'react', 'reaction'),
            '"Emotional testing" कई बार conscious game नहीं — '
            'यह subconscious safety check है: "क्या यह person stable है?"\n\n'
            'Fix करने की कोशिश reaction बढ़ाती है। '
            'Calm presence, boundaries, और consistency ही real answer हैं — performance नहीं।',
        ),
        Insight(
            'women_communication_01', Domain.WOMEN,
            ('बोल', 'कह', 'feel', 'emotion', 'communicat', 'सुन', 'बात', 'समझ नहीं'),
            'कई बार वो problem solve नहीं चाहती — witness चाहती है।\n\n'
            'जब तुम हर feeling को task बनाते हो, वो shut down हो सकती है। '
            'पहले presence, फिर perspective — अगर माँगी जाए तो।',
        ),
        Insight(
            'women_attraction_01', Domain.WOMEN,
            ('attract', 'like', 'पसंद', 'impress', 'interest', 'chase', 'पीछे'),
            'Attraction primarily felt safety और polarity से आती है।\n\n'
            'जो आदमी खुद में grounded है — जिसे अपना direction पता है, '
            'जो हर बात पर approve नहीं माँगता — '
            'वो naturally attractive होता है। '
            'Performance kills attraction; presence builds it।',
            weight=1.1,
        ),
        # Additional insights for expanded knowledge base
        Insight(
            'women_boundaries_01', Domain.WOMEN,
            ('boundary', 'limit', 'no', 'refuse', 'say no', 'नहीं'),
            'Healthy boundaries respect attract करती हैं।\n\n'
            'जो आदमी "no" कहने में comfortable है, '
            'वो "yes" को valuable बनाता है। '
            'People-pleasing attraction kill करता है क्योंकि यह weakness signal करता है।',
            weight=1.05,
        ),
        Insight(
            'women_space_01', Domain.WOMEN,
            ('space', 'distance', 'time', 'give space', 'दूरी'),
            'Space देना rejection नहीं — respect है।\n\n'
            'जो आदमी चिपक जाता है, वो insecurity signal करता है। '
            'जो दूर रहता है और अपनी life जीता है, '
            'वो mystery और self-respect signal करता है।',
            weight=1.1,
        ),
        Insight(
            'women_validation_01', Domain.WOMEN,
            ('validation', 'approve', 'please', 'seek', 'मान'),
            'Validation seeking पुरुषों में भी होता है।\n\n'
            'जो आदमी constant approval माँगता है, '
            'वो emotionally dependent feel होता है। '
            'Women stability को prefer करती हैं constant seeking के बजाय।',
            weight=1.05,
        ),
        Insight(
            'women_confidence_01', Domain.WOMEN,
            ('confident', 'shy', 'nervous', 'fear', 'डर'),
            'Confidence नहीं होना normal है — पर overcompensation नहीं।\n\n'
            'जो आदमी अपनी nervousness छुपाने की कोशिश करता है, '
            'वो awkward feel होता है। '
            'Authenticity — even with nervousness — attractive है।',
            weight=1.0,
        ),
        Insight(
            'women_consistency_01', Domain.WOMEN,
            ('consistent', 'change', 'hot', 'cold', 'reliable'),
            'Consistency intensity से ज़्यादा important है।\n\n'
            'जो आदमी predictable है, वो safe feel होता है। '
            'Hot-cold pattern anxiety create करता है। '
            'Steady presence over dramatic gestures।',
            weight=1.1,
        ),
    ),
)