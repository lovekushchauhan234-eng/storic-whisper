"""
Gemini provider for LUPPI 3.0 - Primary intelligence layer.
Uses Google Gemini API with LUPPI personality + knowledge injection.
"""
import time
from typing import Optional
from google import genai
from google.genai import types
from django.conf import settings
from django.http import HttpRequest
from django.core.cache import cache

from ..engine.pipeline import process_message
from ..engine.response import LuppiResponse
from ..prompts import build_full_prompt
from .base import LuppiProvider
from .local import LocalRulesProvider
from ..classifier import classify_domain
from ..emotional import analyze_emotion
from ..intent import detect_intent
from ..memory.session import SessionMemoryStore


class GeminiProvider(LuppiProvider):
    name = 'gemini'

    def __init__(self):
        self.model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash')
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        self.cache_timeout = getattr(settings, 'GEMINI_CACHE_TIMEOUT', 600)  # 10 minutes (increased from 5)

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def respond(self, request: HttpRequest, message: str) -> LuppiResponse:
        if not self.api_key or not self.client:
            # Graceful fallback to local rules
            return LocalRulesProvider().respond(request, message)

        try:
            # Multi-layer caching strategy to reduce API calls
            
            # Layer 1: Exact message cache (fastest)
            cache_key = f"luppi_gemini_{hash(message)}"
            cached_response = cache.get(cache_key)
            if cached_response:
                return self._build_response_from_cache(cached_response, message, request)

            # Get context for prompt building
            memory_store = SessionMemoryStore(request)
            memory = memory_store.load()
            emotion = analyze_emotion(message)
            intent = detect_intent(message, memory)
            classification = classify_domain(message)

            # Layer 2: Emotional-state + domain cache (for similar emotional contexts)
            emotion_domain_key = f"luppi_emotion_{emotion.primary.value}_{classification.domain.value}_{hash(message[:50])}"
            cached_emotion_response = cache.get(emotion_domain_key)
            if cached_emotion_response and intent.confidence < 0.7:
                # Use cached response for low-confidence intents
                return self._build_response_from_cache(cached_emotion_response, message, request)

            # Retrieve relevant insight
            from ..retrieval import retrieve_insight
            from ..domains import Domain
            insight_body = None
            insight_id = None
            domain = classification.domain
            retrieval = None

            if intent.depth.value in ('light', 'full'):
                retrieval = retrieve_insight(
                    message,
                    domain,
                    exclude_ids=memory.used_insight_ids[-16:],
                )
                if retrieval and retrieval.is_relevant:
                    insight_body = retrieval.insight.body
                    insight_id = retrieval.insight.id

            # Retrieve relevant articles
            article_context = self._retrieve_article_context(domain, message)

            # Build the full prompt
            prompt_data = build_full_prompt(
                message=message,
                insight_body=insight_body or '',
                classification=classification,
                emotion=emotion,
                memory=memory,
            )

            # Add article context to prompt
            if article_context:
                prompt_data['article_knowledge'] = article_context

            # Call Gemini API with retry logic
            response = self._call_gemini_with_retry(prompt_data)

            # Cache the response (both layers)
            cache.set(cache_key, {
                'response': response,
                'domain': domain.value if isinstance(domain, Domain) else 'general',
                'emotion': emotion.primary.value,
                'insight_id': insight_id,
            }, self.cache_timeout)
            
            # Also cache in emotion-domain layer for similar contexts
            cache.set(emotion_domain_key, {
                'response': response,
                'domain': domain.value if isinstance(domain, Domain) else 'general',
                'emotion': emotion.primary.value,
                'insight_id': insight_id,
            }, self.cache_timeout // 2)  # Shorter cache for emotion-domain layer

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
                    'articles_used': len(article_context.split('\n')) if article_context else 0,
                },
            )

        except Exception as e:
            # Fallback to local rules on any error
            print(f"Gemini API error: {e}")
            return LocalRulesProvider().respond(request, message)

    def _call_gemini_with_retry(self, prompt_data: dict, max_retries: int = 3) -> str:
        """Call Gemini API with exponential backoff retry logic."""
        for attempt in range(max_retries):
            try:
                # Build the prompt
                full_prompt = self._build_gemini_prompt(prompt_data)

                # Generate response using new SDK
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=types.Part.from_text(text=full_prompt),
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        top_p=0.8,
                        top_k=40,
                        max_output_tokens=1000,
                    ),
                )

                return response.text

            except Exception as e:
                if attempt < max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    raise e

    def _build_gemini_prompt(self, prompt_data: dict) -> str:
        """Build the full prompt for Gemini."""
        parts = []

        # System prompt (LUPPI personality)
        parts.append(f"""You are LUPPI, a psychology intelligence companion.

Your Personality:
- Mechanism-focused, not motivational
- No toxic positivity
- Bilingual: Hindi-English mix is natural
- Grounded explanations
- Human-first: conversation before psychology dump
- Validate emotions without drama

Your Role:
- Provide psychological insights when relevant
- Use natural, conversational language
- Ask follow-up questions to understand deeper
- Be empathetic but not overly emotional
- Focus on mechanisms and understanding

Response Guidelines:
- Keep responses concise (2-3 paragraphs max)
- Use Hindi-English mix naturally
- Avoid emojis unless necessary
- Don't lecture; explore and understand
- Ask one thoughtful follow-up question when appropriate
""")

        # Context
        if 'context' in prompt_data:
            parts.append(f"\nContext:\n{prompt_data['context']}")

        # Knowledge injection (psychology insights)
        if 'knowledge_injection' in prompt_data and prompt_data['knowledge_injection']:
            parts.append(f"\nPsychology Knowledge:\n{prompt_data['knowledge_injection']}")

        # Article knowledge
        if 'article_knowledge' in prompt_data and prompt_data['article_knowledge']:
            parts.append(f"\nArticle Knowledge:\n{prompt_data['article_knowledge']}")

        # User message
        parts.append(f"\nUser Message: {prompt_data['user']}")

        # Instruction
        parts.append("\n\nRespond naturally as LUPPI. Use the knowledge provided but don't copy it verbatim. Adapt it to the conversation context.")

        return "\n".join(parts)

    def _retrieve_article_context(self, domain, message: str) -> str:
        """Retrieve relevant article context based on domain and message with graceful fallback."""
        try:
            from core.models import Article
            from ..text_utils import term_in_text

            # Map LUPPI domains to Article categories
            domain_to_category = {
                'breakup': 'breakup',
                'women': 'women',
                'dark': 'dark',
                'stoic': 'stoic',
                'dopamine': 'dopamine',
                'human': 'human',
                'transform': 'transform',
                'aimind': 'aimind',
                'general': None,  # No specific category
            }

            category = domain_to_category.get(domain.value if hasattr(domain, 'value') else str(domain))
            if not category:
                return ''

            # Query articles by category with error handling
            articles = Article.objects.filter(
                category=category,
                is_published=True
            ).order_by('-created_at')[:5]  # Get 5 most recent

            if not articles:
                return ''

            # Score articles by keyword matching
            message_lower = message.lower()
            scored_articles = []

            for article in articles:
                score = 0
                # Check title
                for word in article.title.lower().split():
                    if term_in_text(word, message_lower):
                        score += 2
                # Check meta description
                if article.meta_description:
                    for word in article.meta_description.lower().split():
                        if term_in_text(word, message_lower):
                            score += 1

                if score > 0:
                    scored_articles.append((article, score))

            # Sort by score and take top 2
            scored_articles.sort(key=lambda x: x[1], reverse=True)
            top_articles = scored_articles[:2]

            if not top_articles:
                return ''

            # Build article context
            context_parts = []
            for article, score in top_articles:
                context_parts.append(f"Article: {article.title}")
                if article.meta_description:
                    context_parts.append(f"Summary: {article.meta_description}")
                # Add first paragraph of content (simplified)
                content_preview = article.content.split('\n')[:3]
                context_parts.append(f"Preview: {' '.join(content_preview)}")
                context_parts.append("---")

            return "\n".join(context_parts)

        except Exception as e:
            print(f"Article retrieval error: {e}")
            return ''

    def _build_response_from_cache(self, cached_data: dict, message: str, request: HttpRequest) -> LuppiResponse:
        """Build response from cached data."""
        # Still need to save to memory
        memory_store = SessionMemoryStore(request)
        memory = memory_store.load()
        memory_store.append_exchange(
            user_message=message,
            assistant_reply=cached_data['response'],
            domain=cached_data['domain'],
            emotion=cached_data['emotion'],
            insight_id=cached_data['insight_id'],
        )

        return LuppiResponse(
            reply=cached_data['response'],
            domain=cached_data['domain'],
            domain_label=cached_data['domain'].capitalize(),
            emotion=cached_data['emotion'],
            insight_id=cached_data['insight_id'],
            provider=self.name,
            confidence=0.9,
            meta={
                'cached': True,
                'session_turns': len([t for t in memory.turns if t.role == 'user']) + 1,
            },
        )
