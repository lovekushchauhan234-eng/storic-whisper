"""
Insight retrieval — only returns insights with real relevance to the message.
"""
import random
from dataclasses import dataclass

from .domains import Domain
from .knowledge.registry import get_domain_knowledge
from .knowledge.types import Insight
from .text_utils import term_in_text

# Minimum score = at least one strong trigger match (not random domain default)
MIN_RELEVANCE_SCORE = 1.45


@dataclass
class RetrievalResult:
    insight: Insight
    score: float

    @property
    def is_relevant(self) -> bool:
        return self.score >= MIN_RELEVANCE_SCORE


def retrieve_insight(
    message: str,
    domain: Domain,
    exclude_ids: list[str] | None = None,
) -> RetrievalResult | None:
    exclude = set(exclude_ids or [])
    text = message.lower()
    dk = get_domain_knowledge(domain)
    candidates: list[tuple[Insight, float]] = []

    for insight in dk.insights:
        if insight.id in exclude:
            continue
        score = 0.0
        for trigger in insight.triggers:
            if term_in_text(trigger, text):
                score += 1.5 * insight.weight
        if score > 0:
            candidates.append((insight, score))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[1], reverse=True)
    top_score = candidates[0][1]
    if top_score < MIN_RELEVANCE_SCORE:
        return None

    top_tier = [c for c in candidates if c[1] >= top_score * 0.85]
    insight, score = random.choice(top_tier)
    return RetrievalResult(insight, score)
