"""
Django management command to test LUPPI configuration.

Usage:
    python manage.py test_luppi
    python manage.py test_luppi --message "I'm feeling anxious"
"""
from django.core.management.base import BaseCommand
from django.http import HttpRequest
from django.test import RequestFactory

from core.luppi import chat
from core.luppi.providers.health_check import check_provider_health, test_provider_response


class Command(BaseCommand):
    help = 'Test LUPPI configuration and provider health'

    def add_arguments(self, parser):
        parser.add_argument(
            '--message',
            type=str,
            default='Hello, can you help me?',
            help='Test message to send to LUPPI',
        )
        parser.add_argument(
            '--health-only',
            action='store_true',
            help='Only check provider health, don\'t send test message',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== LUPPI 3.0 Configuration Test ===\n'))

        # Check provider health
        self.stdout.write('Checking provider health...')
        health = check_provider_health()

        self.stdout.write(f"  Provider: {health['provider']}")
        self.stdout.write(f"  Active: {health['active']}")
        self.stdout.write(f"  Configured: {health['configured']}")

        if health['details']:
            for key, value in health['details'].items():
                self.stdout.write(f"  {key}: {value}")

        if health['error']:
            self.stdout.write(self.style.ERROR(f"  Error: {health['error']}"))
        else:
            self.stdout.write(self.style.SUCCESS('  Provider is healthy'))

        # Test provider response
        if not options['health_only']:
            self.stdout.write('\nTesting provider response...')
            test_result = test_provider_response(options['message'])

            if test_result['success']:
                self.stdout.write(self.style.SUCCESS('  Test successful'))
                self.stdout.write(f"  Provider: {test_result['provider']}")
                self.stdout.write(f"  Domain: {test_result['domain']}")
                self.stdout.write(f"  Emotion: {test_result['emotion']}")
                self.stdout.write(f"  Confidence: {test_result['confidence']}")
                self.stdout.write(f"  Reply preview: {test_result['reply']}...")
            else:
                self.stdout.write(self.style.ERROR(f"  Test failed: {test_result['error']}"))

        # Summary
        self.stdout.write('\n' + '=' * 50)
        if health['configured'] and health['active']:
            self.stdout.write(self.style.SUCCESS('LUPPI is ready to use!'))
        else:
            self.stdout.write(self.style.WARNING('LUPPI needs configuration.'))
            if not health['configured']:
                self.stdout.write('  - Configure API key in settings or .env')
            if not health['active']:
                self.stdout.write('  - Check provider configuration')
        self.stdout.write('=' * 50 + '\n')
