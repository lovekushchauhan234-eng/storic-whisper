"""
Anthropic Claude provider — generative AI integration for LUPPI 2.0.
Uses Claude API with LUPPI personality + knowledge injection + session memory.
"""
import httpx
from django.conf import settings
from django.http import HttpRequest

from ..engine.pipeline import process_message
from ..engine.response import LuppiResponse
from ..prompts import build_full_prompt
from .base import LuppiProvider
from .local import LocalRulesProvider
from ..classifier import classify_domain
from ..emotional import analyze_emotion
from ..intent import detect_intent
from ..memory.session import SessionMemoryStore


class AnthropicProvider(LuppiProvider):
    name = 'anthropic'

    def respond(self, request: HttpRequest, message: str) -> LuppiResponse:
        api_key = getattr(settings, 'ANTHROPIC_API_KEY', None)
        if not api_key:
            # Graceful fallback until API is configured
            return LocalRulesProvider().respond(request, message)

        try:
            # Get context for prompt building
            memory_store = SessionMemoryStore(request)
            memory = memory_store.load()
            emotion = analyze_emotion(message)
            intent = detect_intent(message, memory)
            classification = classify_domain(message)

            # Retrieve relevant insight if needed
            from ..retrieval import retrieve_insight
            from ..domains import Domain
            insight_body = None
            insight_id = None
            domain = classification.domain

            if intent.depth.value in ('light', 'full'):
                retrieval = retrieve_insight(
                    message,
                    domain,
                    exclude_ids=memory.used_insight_ids[-8:],
                )
                if retrieval and retrieval.is_relevant:
                    insight_body = retrieval.insight.body
                    insight_id = retrieval.insight.id

            # Build the full prompt
            prompt_data = build_full_prompt(
                message=message,
                insight_body=insight_body or '',
                classification=classification,
                emotion=emotion,
                memory=memory,
            )

            # Call Claude API
            response = self._call_claude_api(prompt_data, api_key)

            # Save to memory
            memory_store.append_exchange(
                user_message=message,
                assistant_reply=response,
                domain=domain.value if isinstance(domain, Domain) else 'general',
                emotion=emotion.primary.value,
                insight_id=insight_id,
            )

            return LuppiResponse(
                reply=response,
                domain=domain.value if isinstance(domain, Domain) else 'general',
                domain_label=domain.value if isinstance(domain, Domain) else 'General',
                emotion=emotion.primary.value,
                insight_id=insight_id,
                provider=self.name,
                confidence=intent.confidence,
                meta={
                    'intent': intent.intent.value,
                    'depth': intent.depth.value,
                    'reason': intent.reason,
                    'retrieval_score': getattr(retrieval, 'score', 0) if retrieval else 0,
                    'session_turns': len([t for t in memory.turns if t.role == 'user']) + 1,
                },
            )

        except Exception as e:
            # Fallback to local rules on any error
            return LocalRulesProvider().respond(request, message)

    def _call_claude_api(self, prompt_data: dict, api_key: str) -> str:
        """Call Anthropic Claude Messages API."""
        headers = {
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json',
        }

        # Build messages array for Claude
        messages = [
            {
                'role': 'user',
                'content': f"{prompt_data['context']}\n\n{prompt_data['knowledge_injection']}\n\nUser message: {prompt_data['user']}"
            }
        ]

        payload = {
            'model': 'claude-3-haiku-20240307',  # Use Haiku for speed/cost
            'max_tokens': 1000,
            'system': prompt_data['system'],
            'messages': messages,
            'temperature': 0.7,  # Balanced creativity and consistency
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data['content'][0]['text']
