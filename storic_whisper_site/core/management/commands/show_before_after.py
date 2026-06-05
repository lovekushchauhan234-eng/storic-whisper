from django.core.management.base import BaseCommand
from django.http import HttpRequest
from django.contrib.sessions.backends.db import SessionStore
from core.luppi import chat


class Command(BaseCommand):
    help = 'Show before/after responses for specific psychological concept test cases'

    def handle(self, *args, **options):
        test_cases = [
            'gaslighting signs',
            'narcissist',
            'secure attachment',
            'CBT',
            'emotional awareness',
            'coping mechanisms',
        ]

        # Create mock request with proper session (same approach as stress test)
        class MockRequest:
            def __init__(self):
                self.session = SessionStore()
                self.session_key = self.session.session_key
                self.META = {'REMOTE_ADDR': '127.0.0.1'}

        request = MockRequest()

        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('BEFORE/AFTER RESPONSE COMPARISON'))
        self.stdout.write(self.style.SUCCESS('=' * 80))

        for message in test_cases:
            # Get response
            response = chat(request, message, provider='local')
            
            self.stdout.write(f'\n{self.style.WARNING("-" * 80)}')
            self.stdout.write(f'{self.style.WARNING(f"Input: {message}")}')
            self.stdout.write(f'\n{self.style.SUCCESS("BEFORE (Robotic Fallback):")}')
            
            # Show what the old response would have been
            if 'gaslighting' in message.lower() or 'narcissist' in message.lower():
                old_response = 'Hmm, achha 😊\nAur batao....'
            elif 'secure attachment' in message.lower() or 'cbt' in message.lower():
                old_response = 'सुन रहा हूँ — बताओ थोड़ा और 😊...'
            elif 'emotional awareness' in message.lower() or 'coping mechanisms' in message.lower():
                old_response = 'Hmm, achha 😊\nAur batao....'
            else:
                old_response = 'Yeh topic hai 😊\nBatao thoda detail mein...'
            
            self.stdout.write(f'{self.style.ERROR(old_response)}')
            
            self.stdout.write(f'\n{self.style.SUCCESS("AFTER (Natural Response):")}')
            self.stdout.write(f'{self.style.SUCCESS(response.reply)}')
            
            intent_val = response.meta.get('intent', 'N/A')
            depth_val = response.meta.get('depth', 'N/A')
            self.stdout.write(f'\n{self.style.SUCCESS(f"Intent: {intent_val}")}')
            self.stdout.write(f'{self.style.SUCCESS(f"Depth: {depth_val}")}')

        self.stdout.write(f'\n{self.style.SUCCESS("=" * 80)}')
