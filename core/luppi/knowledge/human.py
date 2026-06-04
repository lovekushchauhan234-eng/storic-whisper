from ..domains import Domain
from .types import DomainKnowledge, Insight

HUMAN_KNOWLEDGE = DomainKnowledge(
    domain=Domain.HUMAN,
    principles=(
        'Behavior follows incentives and fear more than stated values.',
        'Status seeking is ancient software, not character flaw.',
        'Loneliness is often depth starvation.',
    ),
    insights=(
        Insight(
            'human_status_01', Domain.HUMAN,
            ('status', 'ego', 'impress', 'दिख', 'respect'),
            'Status chase shameful नहीं — evolutionary है।\n\n'
            'Problem तब है जब outer performance inner life replace कर दे। '
            'जो सबको impress करता है, किसी के साथ real नहीं रहता।',
        ),
        Insight(
            'human_loneliness_01', Domain.HUMAN,
            ('lonely', 'अकेला', 'alone', 'empty', 'कोई नहीं'),
            '500 connections, zero witness — modern loneliness का shape।\n\n'
            'Brain isolation को threat मानता है; तब तुम clingy या numb हो सकते हो। '
            'Depth एक conversation से शुरू हो सकती है — perfect social life से नहीं।',
            weight=1.1,
        ),
        Insight(
            'human_crowd_01', Domain.HUMAN,
            ('crowd', 'group', 'भीड', 'follow', 'herd'),
            'Crowds individuality नहीं खोते — responsibility खोते हैं।\n\n'
            '“सब कर रहे हैं” brain का oldest hack है। '
            'Independent thinking expensive है — इसीलिए rare लगती है।',
        ),
        Insight(
            'human_validation_01', Domain.HUMAN,
            ('validation', 'like', 'approval', 'मान'),
            'Validation addiction का hunger कभी full नहीं होता — '
            'क्योंकि बाहर की approval अंदर की emptiness fix नहीं करती।',
        ),
    ),
)
