from dataclasses import dataclass, field

from ..domains import Domain


@dataclass(frozen=True)
class Insight:
  """Atomic knowledge unit — future corpus ingestion maps to this shape."""
  id: str
  domain: Domain
  triggers: tuple[str, ...]
  body: str
  weight: float = 1.0
  tags: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DomainKnowledge:
  domain: Domain
  principles: tuple[str, ...]
  insights: tuple[Insight, ...]
