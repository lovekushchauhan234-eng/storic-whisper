"""
LUPPI knowledge domains — canonical IDs aligned with Storic Whisper pillars.
"""
from dataclasses import dataclass
from enum import Enum


class Domain(str, Enum):
    BREAKUP = 'breakup'
    WOMEN = 'women'
    DARK = 'dark'
    STOIC = 'stoic'
    DOPAMINE = 'dopamine'
    HUMAN = 'human'
    TRANSFORM = 'transform'
    AIMIND = 'aimind'
    GENERAL = 'general'


@dataclass(frozen=True)
class DomainMeta:
    id: Domain
    label: str
    label_hi: str
    description: str


DOMAIN_REGISTRY: dict[Domain, DomainMeta] = {
    Domain.BREAKUP: DomainMeta(
        Domain.BREAKUP,
        'Breakup Psychology',
        'Breakup & Attachment',
        'Attachment pain, grief, no-contact, trauma bonds, self-worth.',
    ),
    Domain.WOMEN: DomainMeta(
        Domain.WOMEN,
        'Women Psychology',
        'Women Psychology',
        'Attachment styles, signals, attraction, emotional communication.',
    ),
    Domain.DARK: DomainMeta(
        Domain.DARK,
        'Dark Psychology Defense',
        'Dark Psychology',
        'Manipulation, gaslighting, narcissism, protection systems.',
    ),
    Domain.STOIC: DomainMeta(
        Domain.STOIC,
        'Stoicism',
        'Stoicism',
        'Emotional control, discipline, detachment, inner stability.',
    ),
    Domain.DOPAMINE: DomainMeta(
        Domain.DOPAMINE,
        'Dopamine & Modern Mind',
        'Dopamine & Addiction',
        'Overstimulation, cheap dopamine, attention collapse.',
    ),
    Domain.HUMAN: DomainMeta(
        Domain.HUMAN,
        'Human Behavior',
        'Human Behavior',
        'Status, loneliness, crowd psychology, fear, validation.',
    ),
    Domain.TRANSFORM: DomainMeta(
        Domain.TRANSFORM,
        'Self-Transformation',
        'Self-Transformation',
        'Identity rebuild, habits, discipline, self-respect.',
    ),
    Domain.AIMIND: DomainMeta(
        Domain.AIMIND,
        'AI + Human Mind',
        'AI + Consciousness',
        'Digital intimacy, emotional AI, future human-AI bonds.',
    ),
    Domain.GENERAL: DomainMeta(
        Domain.GENERAL,
        'General Psychology',
        'Psychology',
        'Open emotional exploration without a fixed domain.',
    ),
}
