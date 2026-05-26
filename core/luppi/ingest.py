"""
Future knowledge ingestion — books, articles, scripts → Insight records.

Planned pipeline:
  1. Raw text (file/DB) → chunks
  2. Tag with Domain + triggers (manual or NLP)
  3. Validate against Insight schema
  4. Merge into registry or store in KnowledgeChunk model (future)

Not active in Phase 1 — architecture hook only.
"""
from dataclasses import dataclass

from .domains import Domain
from .knowledge.types import Insight


@dataclass
class RawKnowledgeDocument:
    source_id: str
    title: str
    domain: Domain
    body: str
    language: str = 'hi-en'


def document_to_insight(doc: RawKnowledgeDocument, insight_id: str, triggers: tuple[str, ...]) -> Insight:
    return Insight(
        id=insight_id,
        domain=doc.domain,
        triggers=triggers,
        body=doc.body.strip(),
    )
