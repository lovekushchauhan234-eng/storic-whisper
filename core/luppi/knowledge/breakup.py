from ..domains import Domain
from .types import DomainKnowledge, Insight

BREAKUP_KNOWLEDGE = DomainKnowledge(
    domain=Domain.BREAKUP,
    principles=(
        'Breakup pain is often nervous-system loss, not logical failure.',
        'No-contact is emotional detox, not punishment.',
        'Attachment can feel like addiction without being “weakness”.',
    ),
    insights=(
        Insight(
            'breakup_attachment_01', Domain.BREAKUP,
            ('attach', 'attachment', 'छोड़', 'miss', 'याद', 'वापस', 'bond', 'addict'),
            'जो तुम miss करते हो अक्सर सिर्फ एक person नहीं — '
            'वो identity, routine और emotional safety होती है जो उनके साथ बनी थी।\n\n'
            'Brain oxytocin और dopamine को उनके साथ link कर चुका होता है। '
            'Breakup के बाद वही pathways fire होती हैं — इसीलिए “logic” काम नहीं करता। '
            'यह biology है, character defect नहीं।',
            weight=1.2,
        ),
        Insight(
            'breakup_nocontact_01', Domain.BREAKUP,
            ('no contact', 'nocontact', 'contact', 'text', 'check', 'stalk', 'देख'),
            'No-contact सबसे कठिन इसलिए है क्योंकि यह withdrawal जैसा feel होता है।\n\n'
            'हर बार जब तुम उन्हें check करते हो — message, story, photo — '
            'तुम्हारा brain healing को restart करता है। '
            'Distance nervous system को reset करने का space देती है। '
            'यह उन्हें punish करना नहीं — खुद को वापस लाना है।',
            weight=1.15,
        ),
        Insight(
            'breakup_trauma_bond_01', Domain.BREAKUP,
            ('trauma', 'toxic', 'cycle', 'वापस', 'फिर', 'again', 'on off', 'hot cold'),
            'Trauma bond intermittent reinforcement से बनता है — '
            'कभी warmth, कभी withdrawal।\n\n'
            'यह pattern slot machines जैसा है: uncertainty dopamine spike करती है। '
            'तुम person को miss नहीं करते — तुम relief की possibility miss करते हो। '
            'इसे पहचानना पहला defense है।',
            weight=1.1,
        ),
        Insight(
            'breakup_grief_01', Domain.BREAKUP,
            ('grief', 'heal', 'time', 'दर्द', 'रो', 'sad', 'टूट'),
            'Grief linear नहीं होती — waves आती हैं। '
            'एक दिन clarity, अगले दिन फिर heaviness।\n\n'
            'Healing का मतलब उन्हें भूलना नहीं — '
            'उनसे जुड़ी अपनी story को slowly rewrite करना है। '
            'Pain को avoid मत करो; उसे witness करो — बिना drama के।',
        ),
        Insight(
            'breakup_worth_01', Domain.BREAKUP,
            ('worth', 'value', 'खुद', 'self', 'respect', 'चुन'),
            'Breakup के बाद सबसे dangerous story यह है: “मैं enough नहीं था।”\n\n'
            'Relationship end होना तुम्हारी value define नहीं करता — '
            'यह compatibility, timing, maturity और sometimes manipulation का output होता है। '
            'Self-worth तब बनती है जब तुम खुद को वापस choose करना शुरू करते हो — छोटे acts से।',
        ),
    ),
)
from ..domains import Domain
from .types import DomainKnowledge, Insight

BREAKUP_KNOWLEDGE = DomainKnowledge(
    domain=Domain.BREAKUP,
    principles=(
        'Breakup pain is nervous-system loss, not logical failure.',
        'No-contact is emotional detox, not punishment.',
        'Attachment can feel like addiction without being weakness.',
        'Healing is not linear — waves are normal.',
        'Self-worth is rebuilt through small daily choices.',
    ),
    insights=(
        Insight(
            'breakup_attachment_01', Domain.BREAKUP,
            ('attach', 'attachment', 'छोड़', 'miss', 'याद', 'वापस', 'bond', 'addict', 'bhool', 'भूल'),
            'जो तुम miss करते हो अक्सर सिर्फ एक person नहीं — '
            'वो identity, routine और emotional safety होती है जो उनके साथ बनी थी।\n\n'
            'Brain oxytocin और dopamine को उनके साथ link कर चुका होता है। '
            'Breakup के बाद वही pathways fire होती हैं — इसीलिए "logic" काम नहीं करता। '
            'यह biology है, character defect नहीं।',
            weight=1.2,
        ),
        Insight(
            'breakup_nocontact_01', Domain.BREAKUP,
            ('no contact', 'nocontact', 'contact', 'text', 'check', 'stalk', 'देख', 'message', 'call'),
            'No-contact सबसे कठिन इसलिए है क्योंकि यह withdrawal जैसा feel होता है।\n\n'
            'हर बार जब तुम उन्हें check करते हो — message, story, photo — '
            'तुम्हारा brain healing को restart करता है। '
            'Distance nervous system को reset करने का space देती है। '
            'यह उन्हें punish करना नहीं — खुद को वापस लाना है।',
            weight=1.15,
        ),
        Insight(
            'breakup_trauma_bond_01', Domain.BREAKUP,
            ('trauma', 'toxic', 'cycle', 'वापस', 'फिर', 'again', 'on off', 'hot cold', 'छोड़ नहीं', 'छूट नहीं'),
            'Trauma bond intermittent reinforcement से बनता है — '
            'कभी warmth, कभी withdrawal।\n\n'
            'यह pattern slot machines जैसा है: uncertainty dopamine spike करती है। '
            'तुम person को miss नहीं करते — तुम relief की possibility miss करते हो। '
            'इसे पहचानना पहला defense है।',
            weight=1.1,
        ),
        Insight(
            'breakup_grief_01', Domain.BREAKUP,
            ('grief', 'heal', 'time', 'दर्द', 'रो', 'sad', 'टूट', 'रो रहा', 'cry', 'crying'),
            'Grief linear नहीं होती — waves आती हैं। '
            'एक दिन clarity, अगले दिन फिर heaviness।\n\n'
            'Healing का मतलब उन्हें भूलना नहीं — '
            'उनसे जुड़ी अपनी story को slowly rewrite करना है। '
            'Pain को avoid मत करो; उसे witness करो — बिना drama के।',
        ),
        Insight(
            'breakup_worth_01', Domain.BREAKUP,
            ('worth', 'value', 'खुद', 'self', 'respect', 'चुन', 'enough', 'कमी', 'मेरी गलती'),
            'Breakup के बाद सबसे dangerous story यह है: "मैं enough नहीं था।"\n\n'
            'Relationship end होना तुम्हारी value define नहीं करता — '
            'यह compatibility, timing, maturity और sometimes manipulation का output होता है। '
            'Self-worth तब बनती है जब तुम खुद को वापस choose करना शुरू करते हो — छोटे acts से।',
        ),
        Insight(
            'breakup_moving_on_01', Domain.BREAKUP,
            ('move on', 'आगे', 'forget', 'new life', 'नई शुरुआत', 'start', 'kaise', 'कैसे'),
            'Moving on एक decision नहीं — एक direction है।\n\n'
            'हर दिन तुम वही choice करते हो: उनकी memory में रहूँ या अपनी life में return करूँ। '
            'दोनों valid feel होते हैं कभी-कभी। '
            'लेकिन जिस दिन तुम खुद के लिए कुछ करते हो — बिना उनकी approval के — '
            'उस दिन healing एक inch आगे बढ़ती है।',
        ),
        Insight(
            'breakup_anger_01', Domain.BREAKUP,
            ('anger', 'गुस्सा', 'hate', 'नफरत', 'betray', 'धोखा', 'झूठ', 'lie', 'cheat', 'चीट'),
            'Anger breakup के बाद valid है — यह grief का एक phase है।\n\n'
            'जो hurt करता है, उसके प्रति गुस्सा आना healthy processing है। '
            'Problem तब है जब anger तुम्हें उनसे connected रखे — '
            'नफरत भी एक attachment है। '
            'Neutrality — indifference — असली freedom है।',
        ),
        Insight(
            'breakup_rebound_01', Domain.BREAKUP,
            ('new person', 'नया', 'new relationship', 'date', 'dating', 'rebound', 'replace'),
            'Rebound relationships अक्सर pain को address नहीं करतीं — '
            'वो उसे temporarily मुँह से दूर करती हैं।\n\n'
            'नई connection में पुराने patterns लेकर जाते हो जब तक '
            'पुरानी attachment को actually process नहीं किया। '
            'Timing नहीं — readiness matter करती है।',
        ),
        Insight(
            'breakup_closure_01', Domain.BREAKUP,
            ('closure', 'बात', 'समझ', 'explain', 'reason', 'क्यों', 'why', 'पता नहीं क्यों'),
            'Closure अक्सर बाहर से नहीं आती — तुम उसे खुद create करते हो।\n\n'
            'उनसे final conversation की उम्मीद रखना '
            'उसी wound को बार-बार open करना है। '
            'Real closure तब आती है जब तुम accept करते हो: '
            '"मुझे शायद कभी पूरा answer नहीं मिलेगा — और मैं फिर भी ठीक हो सकता हूँ।"',
        ),
        Insight(
            'breakup_loneliness_01', Domain.BREAKUP,
            ('अकेला', 'alone', 'lonely', 'रात', 'night', 'silence', 'खालीपन', 'empty'),
            'Breakup के बाद रात सबसे heavy होती है — '
            'क्योंकि distraction कम होते हैं और brain unprocessed emotions surface करता है।\n\n'
            'यह अकेलापन weakness नहीं — यह signal है कि तुम्हें connection की ज़रूरत है: '
            'खुद के साथ पहले, फिर दूसरों के साथ। '
            'उस silence में बैठना — बिना phone उठाए — एक act of courage है।',
        ),
    ),
)