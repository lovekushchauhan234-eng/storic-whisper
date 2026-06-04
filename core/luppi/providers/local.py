from django.http import HttpRequest

from ..engine.pipeline import process_message
from ..engine.response import LuppiResponse
from ..classifier import classify_domain
from ..emotional import analyze_emotion
from .base import LuppiProvider
from .local_responses import get_response


class LocalRulesProvider(LuppiProvider):
    """Phase 1: structured psychology engine without external API."""

    name = 'local'

    def respond(self, request: HttpRequest, message: str) -> LuppiResponse:
        # Use varied response templates instead of repetitive ones
        try:
            classification = classify_domain(message)
            emotion = analyze_emotion(message)
            
            # Get varied response based on domain and emotion
            varied_response = get_response(
                domain=classification.domain.value,
                emotion=emotion.primary.value
            )
            
            # Fall back to pipeline if varied response not available
            if not varied_response or varied_response.startswith("अच्छा सवाल"):
                return process_message(request, message, provider=self.name)
            
            # Return varied response with proper metadata
            return LuppiResponse(
                reply=varied_response,
                domain=classification.domain.value,
                domain_label=classification.domain.value.title(),
                emotion=emotion.primary.value,
                insight_id=None,
                provider=self.name,
                confidence=0.7,
                meta={
                    'intent': 'fallback_varied',
                    'depth': 'light',
                    'reason': 'Using varied response templates for fallback',
                    'retrieval_score': 0,
                    'session_turns': 1,
                    'articles_used': 0,
                },
            )
        except Exception as e:
            # Ultimate fallback to pipeline
            return process_message(request, message, provider=self.name)
