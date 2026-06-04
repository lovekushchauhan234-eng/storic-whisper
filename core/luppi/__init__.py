"""
LUPPI — psychological intelligence layer for Storic Whisper.

Usage:
    from core.luppi import chat
    response = chat(request, "why does breakup hurt so much")
"""
from django.http import HttpRequest

from .engine.response import LuppiResponse
from .providers import get_provider


def chat(request: HttpRequest, message: str, provider: str | None = None) -> LuppiResponse:
    """
    Main entry point for LUPPI conversations.

    Args:
        request: Django HTTP request
        message: User message
        provider: Optional provider override ('local', 'anthropic', 'gemini')

    Returns:
        LuppiResponse with reply, metadata, and context
    """
    if provider:
        from .providers.local import LocalRulesProvider
        if provider == 'local':
            return LocalRulesProvider().respond(request, message)
        elif provider == 'anthropic':
            from .providers.anthropic import AnthropicProvider
            return AnthropicProvider().respond(request, message)
        elif provider == 'gemini':
            from .providers.gemini import GeminiProvider
            return GeminiProvider().respond(request, message)

    return get_provider().respond(request, message)


__all__ = ['chat', 'LuppiResponse']
