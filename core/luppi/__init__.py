"""
LUPPI — psychological intelligence layer for Storic Whisper.

Usage:
    from core.luppi import chat
    response = chat(request, "why does breakup hurt so much")
"""
from django.http import HttpRequest

from .engine.response import LuppiResponse
from .providers import get_provider


def chat(request: HttpRequest, message: str) -> LuppiResponse:
    return get_provider().respond(request, message)


__all__ = ['chat', 'LuppiResponse']
