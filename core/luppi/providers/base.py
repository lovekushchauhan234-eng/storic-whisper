"""
LLM provider interface — swap LocalRulesProvider for AnthropicProvider later.
"""
from abc import ABC, abstractmethod

from django.http import HttpRequest

from ..engine.response import LuppiResponse


class LuppiProvider(ABC):
    name: str = 'base'

    @abstractmethod
    def respond(self, request: HttpRequest, message: str) -> LuppiResponse:
        ...
