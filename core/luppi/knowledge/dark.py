from ..domains import Domain
from .types import DomainKnowledge, Insight

DARK_KNOWLEDGE = DomainKnowledge(
    domain=Domain.DARK,
    principles=(
        'Awareness is protection; ignorance is vulnerability.',
        'Manipulation exploits guilt, fear, and identity confusion.',
        'Gray rock reduces supply to narcissistic dynamics.',
    ),
    insights=(
        Insight(
            'dark_gaslight_01', Domain.DARK,
            ('gaslight', 'reality', 'crazy', 'पागल', 'याद', 'नहीं कहा'),
            'Gaslighting का core move reality को unstable बनाना है।\n\n'
            'अगर किसी के साथ तुम consistently confused, guilty और self-doubting रहते हो — '
            'यह love का symptom नहीं हो सकता। '
            'Trust अपनी memory और body signals को — सिर्फ उनके narrative को नहीं।',
            weight=1.2,
        ),
        Insight(
            'dark_lovebomb_01', Domain.DARK,
            ('love bomb', 'bombing', 'fast', 'जल्दी', 'perfect', 'soulmate'),
            'Love bombing: intense idealization, future promises, constant availability — फिर sudden cool-down।\n\n'
            'Real bonding slow और imperfect होती है। '
            'जो बहुत तेज़ “perfect” feel हो, वो अक्सर attachment hook है, intimacy नहीं।',
        ),
        Insight(
            'dark_narcissism_01', Domain.DARK,
            ('narcis', 'ego', 'triang', 'dark triad', 'psychopath'),
            'Narcissistic dynamics में तुम object बन जाते हो — witness नहीं।\n\n'
            'Patterns: हर बात उन पर आती है, empathy perform होती है पर feel नहीं होती, '
            'criticism unbearable। '
            'Goal जीतना नहीं — distance और boring boundaries (gray rock)।',
        ),
        Insight(
            'dark_guilt_01', Domain.DARK,
            ('guilt', 'गिल्ट', 'blame', 'दोष', 'manipul'),
            'Guilt tripping तुम्हें अपनी boundaries छोड़वाती है — “अगर तुम प्यार करते तो…”\n\n'
            'Healthy love guilt को weapon नहीं बनाती। '
            '“मुझे यह accept नहीं” — explanation की ज़रूरत नहीं।',
        ),
        Insight(
            'dark_grayrock_01', Domain.DARK,
            ('gray rock', 'protect', 'बच', 'toxic', 'escape'),
            'Gray Rock: emotionally uninteresting बन जाओ — not cruel, just flat।\n\n'
            'Manipulators drama और reaction feed पर रहते हैं। '
            'जब supply कम हो, वे अक्सर खुद move on करते हैं या escalate करते हैं — '
            'तब boundaries और distance critical हैं।',
        ),
    ),
)
