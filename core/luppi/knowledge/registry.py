"""
Knowledge registry — single import point for all domains.
Future: load additional chunks from DB / files via ingest pipeline.
"""
from ..domains import Domain
from .types import DomainKnowledge, Insight
from .breakup import BREAKUP_KNOWLEDGE
from .women import WOMEN_KNOWLEDGE
from .dark import DARK_KNOWLEDGE
from .stoic import STOIC_KNOWLEDGE
from .dopamine import DOPAMINE_KNOWLEDGE
from .human import HUMAN_KNOWLEDGE
from .transform import TRANSFORM_KNOWLEDGE
from .aimind import AIMIND_KNOWLEDGE
from .general import GENERAL_KNOWLEDGE
from .techniques import TECHNIQUES_KNOWLEDGE
from .childhood import CHILDHOOD_KNOWLEDGE
from .anxiety import ANXIETY_KNOWLEDGE
from .self_esteem import SELF_ESTEEM_KNOWLEDGE
from .family import FAMILY_KNOWLEDGE

ALL_KNOWLEDGE: tuple[DomainKnowledge, ...] = (
    BREAKUP_KNOWLEDGE,
    WOMEN_KNOWLEDGE,
    DARK_KNOWLEDGE,
    STOIC_KNOWLEDGE,
    DOPAMINE_KNOWLEDGE,
    HUMAN_KNOWLEDGE,
    TRANSFORM_KNOWLEDGE,
    AIMIND_KNOWLEDGE,
    GENERAL_KNOWLEDGE,
    TECHNIQUES_KNOWLEDGE,
    CHILDHOOD_KNOWLEDGE,
    ANXIETY_KNOWLEDGE,
    SELF_ESTEEM_KNOWLEDGE,
    FAMILY_KNOWLEDGE,
)

_BY_DOMAIN: dict[Domain, DomainKnowledge] = {k.domain: k for k in ALL_KNOWLEDGE}

# Classifier keyword weights (domain-level)
DOMAIN_KEYWORDS: dict[Domain, tuple[str, ...]] = {
    Domain.BREAKUP: (
        'breakup', 'ex', 'छोड', 'relationship', 'no contact', 'attach', 'heart',
        'गर्लफ्रैंड', 'बॉयफ्रेंड', 'love', 'pyaar', 'दर्द', 'heal',
    ),
    Domain.WOMEN: (
        'women', 'girl', 'लड़की', 'she', 'her', 'mixed signal', 'attraction',
        'girlfriend', 'वो कह', 'feminine',
    ),
    Domain.DARK: (
        'gaslight', 'narcis', 'manipul', 'toxic', 'dark', 'triang', 'psychopath',
        'control', 'abuse', 'धोखा',
    ),
    Domain.STOIC: (
        'stoic', 'marcus', 'philosophy', 'discipline', 'control', 'amor', 'fate',
        'silence', 'detach',
    ),
    Domain.DOPAMINE: (
        'dopamine', 'reel', 'scroll', 'porn', 'addict', 'phone', 'instagram',
        'focus', 'brain fog', 'stimulation',
    ),
    Domain.HUMAN: (
        'behavior', 'crowd', 'status', 'lonely', 'validation', 'lie', 'fear',
        'समाज', 'लोग',
    ),
    Domain.TRANSFORM: (
        'transform', 'habit', 'identity', 'discipline', 'respect', 'worth',
        'change', 'rebuild', 'खुद',
    ),
    Domain.AIMIND: (
        'ai', 'luppi', 'chatgpt', 'conscious', 'robot', 'digital', 'companion',
    ),
}


def get_domain_knowledge(domain: Domain) -> DomainKnowledge:
    return _BY_DOMAIN.get(domain, GENERAL_KNOWLEDGE)


def all_insights() -> list[Insight]:
    out: list[Insight] = []
    for dk in ALL_KNOWLEDGE:
        out.extend(dk.insights)
    return out
