from django.conf import settings

from .anthropic import AnthropicProvider
from .base import LuppiProvider
from .gemini import GeminiProvider
from .local import LocalRulesProvider


def get_provider() -> LuppiProvider:
    name = getattr(settings, 'LUPPI_PROVIDER', 'local').lower()
    if name == 'gemini':
        return GeminiProvider()
    if name == 'anthropic':
        return AnthropicProvider()
    return LocalRulesProvider()
