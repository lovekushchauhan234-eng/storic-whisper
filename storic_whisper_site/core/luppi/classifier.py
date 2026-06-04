"""
Domain classifier — only for messages that need psychological routing.
"""
from dataclasses import dataclass

from .domains import Domain, DOMAIN_REGISTRY
from .knowledge.registry import DOMAIN_KEYWORDS, get_domain_knowledge
from .text_utils import term_in_text

MIN_DOMAIN_SCORE = 2.0


@dataclass
class ClassificationResult:
    domain: Domain
    confidence: float
    scores: dict[str, float]

    @property
    def is_strong(self) -> bool:
        return self.confidence >= 0.55 and max(self.scores.values(), default=0) >= MIN_DOMAIN_SCORE


def classify_domain(message: str) -> ClassificationResult:
    text = message.lower()
    scores: dict[Domain, float] = {}

    for domain, keywords in DOMAIN_KEYWORDS.items():
        if domain == Domain.GENERAL:
            continue
        hit = sum(1.2 for kw in keywords if term_in_text(kw, text))
        if hit:
            scores[domain] = hit

    for domain in list(scores.keys()):
        dk = get_domain_knowledge(domain)
        for insight in dk.insights:
            trigger_hits = sum(1 for t in insight.triggers if term_in_text(t, text))
            if trigger_hits:
                scores[domain] = scores.get(domain, 0) + trigger_hits * insight.weight

    if not scores:
        return ClassificationResult(Domain.GENERAL, 0.0, {Domain.GENERAL.value: 0.0})

    primary = max(scores, key=scores.get)
    total = sum(scores.values()) or 1.0
    confidence = scores[primary] / total

    return ClassificationResult(
        domain=primary,
        confidence=round(confidence, 3),
        scores={d.value: round(s, 3) for d, s in scores.items()},
    )


def domain_label(domain: Domain) -> str:
    meta = DOMAIN_REGISTRY.get(domain)
    return meta.label_hi if meta else domain.value
