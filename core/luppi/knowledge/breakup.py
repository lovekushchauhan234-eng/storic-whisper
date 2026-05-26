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
