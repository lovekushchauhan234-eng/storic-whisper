from dataclasses import dataclass, field
from typing import Any


@dataclass
class LuppiResponse:
    reply: str
    domain: str
    domain_label: str
    emotion: str
    insight_id: str | None
    provider: str
    confidence: float = 0.0
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            'reply': self.reply,
            'domain': self.domain,
            'domain_label': self.domain_label,
            'emotion': self.emotion,
            'insight_id': self.insight_id,
            'provider': self.provider,
            'confidence': self.confidence,
            'meta': self.meta,
        }
