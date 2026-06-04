"""
Health check for LUPPI providers.
Verifies that the configured provider is active and working.
"""
from django.conf import settings
from django.contrib.sessions.backends.cache import SessionStore
from django.http import HttpRequest
from django.test import RequestFactory

from .factory import get_provider
from .base import LuppiProvider


def check_provider_health() -> dict:
    """
    Check the health of the configured LUPPI provider.

    Returns:
        dict with provider status and details
    """
    provider_name = getattr(settings, 'LUPPI_PROVIDER', 'local').lower()
    result = {
        'provider': provider_name,
        'active': False,
        'configured': False,
        'error': None,
        'details': {},
    }

    try:
        provider = get_provider()
        result['active'] = True
        result['configured'] = True
        result['details']['name'] = provider.name

        # Check provider-specific configuration
        if provider_name == 'gemini':
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            result['details']['api_key_configured'] = api_key is not None
            result['details']['model'] = getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash')
            if not api_key:
                result['configured'] = False
                result['error'] = 'GEMINI_API_KEY not configured'

        elif provider_name == 'anthropic':
            api_key = getattr(settings, 'ANTHROPIC_API_KEY', None)
            result['details']['api_key_configured'] = api_key is not None
            if not api_key:
                result['configured'] = False
                result['error'] = 'ANTHROPIC_API_KEY not configured'

        elif provider_name == 'local':
            result['details']['fallback_mode'] = True

    except Exception as e:
        result['active'] = False
        result['error'] = str(e)

    return result


def test_provider_response(message: str = "Hello, can you help me?") -> dict:
    """
    Test the provider with a simple message.

    Args:
        message: Test message to send

    Returns:
        dict with test results
    """
    factory = RequestFactory()
    request = factory.get('/')
    
    # Create a simple session object with session_key
    class SimpleSession:
        def __init__(self):
            self.session_key = 'test_session_key'
            self.modified = False
        
        def get(self, key, default=None):
            return default
        
        def __setitem__(self, key, value):
            pass
    
    request.session = SimpleSession()
    request.user = type('User', (), {'is_authenticated': False})()

    try:
        provider = get_provider()
        response = provider.respond(request, message)

        return {
            'success': True,
            'provider': provider.name,
            'reply': response.reply[:200],  # First 200 chars
            'domain': response.domain,
            'emotion': response.emotion,
            'confidence': response.confidence,
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
        }
