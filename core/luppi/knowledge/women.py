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
            'वो naturally interesting होता है। '
            'Performance attraction kill करती है; presence build करती है।',
            weight=1.1,
        ),
        Insight(
            'women_hypergamy_01', Domain.WOMEN,
            ('hypergam', 'upgrade', 'better option', 'replace', 'status', 'rich', 'successful'),
            'Hypergamy एक evolutionary tendency है — '
            'partner में security, status और growth देखना।\n\n'
            'यह "gold digger" label नहीं — यह biology है। '
            'जो men इसे bitter होकर देखते हैं, वो अपनी growth avoid करते हैं। '
            'जो इसे understand करके खुद को build करते हैं — वो actually attractive बनते हैं।',
        ),
        Insight(
            'women_push_pull_01', Domain.WOMEN,
            ('push pull', 'दूर', 'पास', 'आता है जाता है', 'available', 'unavailable', 'hot cold'),
            'Push-pull dynamic तब बनता है जब एक person consistently '
            'available-unavailable pattern create करे।\n\n'
            'Brain unpredictability को reward की तरह process करता है — '
            'इसीलिए यह addictive लगता है। '
            'Healthy relationship में security boring नहीं लगती — '
            'वो foundation होती है।',
        ),
        Insight(
            'women_breakup_01', Domain.WOMEN,
            ('वो चली गई', 'she left', 'छोड़ दिया', 'breakup', 'end', 'खत्म', 'reject'),
            'जब वो छोड़ के जाती है, सबसे dangerous reaction है: '
            '"मैंने क्या गलत किया?" पर obsess करना।\n\n'
            'कभी-कभी कोई गलती नहीं होती — timing, compatibility, '
            'या उनकी internal situation matter करती है। '
            'Post-mortem उतना ही करो जितना actually कुछ सीखा जाए — '
            'फिर forward।',
        ),
        Insight(
            'women_silence_01', Domain.WOMEN,
            ('silent', 'चुप', 'reply नहीं', 'seen', 'ghosting', 'ghost', 'बात नहीं'),
            'जब वो suddenly silent हो जाए — '
            'दो possibilities हैं: processing कर रही है, या distance बना रही है।\n\n'
            'Flooding उन्हें messages से response नहीं लाता — '
            'वो और retreat करती हैं। '
            'एक clear, non-needy message भेजो और space दो। '
            'Response उनका choice है — pursue करना तुम्हारा choice था।',
        ),
    ),
)