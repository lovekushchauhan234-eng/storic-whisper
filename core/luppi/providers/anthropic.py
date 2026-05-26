"""
Anthropic Claude provider — stub for Phase 3.
Will use prompts.build_full_prompt() + knowledge injection + session memory.
"""
from django.conf import settings
from django.http import HttpRequest

from ..engine.pipeline import process_message
from ..engine.response import LuppiResponse
from .base import LuppiProvider
from .local import LocalRulesProvider


class AnthropicProvider(LuppiProvider):
    name = 'anthropic'

    def respond(self, request: HttpRequest, message: str) -> LuppiResponse:
        api_key = getattr(settings, 'ANTHROPIC_API_KEY', None)
        if not api_key:
            # Graceful fallback until API is configured
            return LocalRulesProvider().respond(request, message)
        # TODO: httpx call to Messages API with build_system_prompt() + memory
        return process_message(request, message, provider='anthropic_pending')
