from ..domains import Domain
from .types import DomainKnowledge, Insight

STOIC_KNOWLEDGE = DomainKnowledge(
    domain=Domain.STOIC,
    principles=(
        'Control responses, not outcomes.',
        'Silence is strength when speech adds noise.',
        'Discipline is self-respect made repeatable.',
    ),
    insights=(
        Insight(
            'stoic_control_01', Domain.STOIC,
            ('control', 'marcus', 'stoic', 'dichotomy', 'बदल'),
            'Dichotomy of control: बाहर की दुनिया नहीं — तुम्हारी interpretation और action।\n\n'
            'Breakup, rejection, दूसरे के mood — बाहर। '
            'तुम आज क्या consume करते हो, किससे बात करते हो, क्या tolerate करते हो — अंदर। '
            'Power वहीं शुरू होती है जहाँ excuse खत्म होते हैं — शांति से।',
            weight=1.15,
        ),
        Insight(
            'stoic_silence_01', Domain.STOIC,
            ('silence', 'चुप', 'quiet', 'react', 'reply'),
            'जो हर चीज़ का जवाब देता है, वो अपनी energy leak करता है।\n\n'
            'Silence manipulation नहीं — यह self-possession है। '
            'Not every message deserves your nervous system।',
        ),
        Insight(
            'stoic_amor_fati_01', Domain.STOIC,
            ('fate', 'amor', 'accept', 'किस्मत', 'हुआ'),
            'Amor fati: जो हुआ उसे enemy नहीं — material बनाओ।\n\n'
            'दर्द wasted नहीं होती जब तुम उससे depth, boundaries और clarity निकालो। '
            'यह positive thinking नहीं — ruthless honesty है।',
        ),
        Insight(
            'stoic_discipline_01', Domain.STOIC,
            ('discipline', 'routine', 'habit', 'सुबह', 'focus'),
            'Discipline motivation का wait नहीं करती — यह identity का vote है।\n\n'
            'एक छोटा non-negotiable act रोज़ — body को signal: मैं अपनी ज़िंदगी का author हूँ।',
            weight=1.1,
        ),
        # Additional insights for expanded knowledge base
        Insight(
            'stoic_memento_mori_01', Domain.STOIC,
            ('death', 'mortality', 'life', 'time', 'limited'),
            'Memento mori: death की reminder से life precious हो जाती है।\n\n'
            'जब तुम realize करते हो कि time finite है, '
            'trivial matters lose power। '
            'Focus shifts to what actually matters।',
            weight=1.05,
        ),
        Insight(
            'stoic_journaling_01', Domain.STOIC,
            ('journal', 'write', 'reflect', 'evening review', 'लिख'),
            'Evening review: दिन का reflection — क्या गलत हुआ, क्या सीखा।\n\n'
            'Stoics daily review करते थे। '
            'Pattern recognition से improvement होता है। '
            'Write without judgment, observe with clarity।',
            weight=1.0,
        ),
        Insight(
            'stoic_negative_visualization_01', Domain.STOIC,
            ('imagine', 'worst case', 'lose', 'prepare', 'premeditatio'),
            'Premeditatio malorum: worst case imagine करना से fear कम होता है।\n\n'
            'जब तुम worst scenario mentally prepare कर लेते हो, '
            'reality अक्सर less scary होती है। '
            'This is not pessimism — preparation।',
            weight=1.1,
        ),
    ),
)
