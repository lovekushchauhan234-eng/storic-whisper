from django.http import HttpRequest

from ..engine.pipeline import process_message
from ..engine.response import LuppiResponse
from .base import LuppiProvider


class LocalRulesProvider(LuppiProvider):
    """Phase 1: structured psychology engine without external API."""

    name = 'local'

    def respond(self, request: HttpRequest, message: str) -> LuppiResponse:
        # Use the full intent detection pipeline - do NOT bypass it
        return process_message(request, message, provider=self.name)
