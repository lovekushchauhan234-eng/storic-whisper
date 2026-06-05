"""
Test LUPPI with the real conversation that failed.
"""
from django.core.management.base import BaseCommand
from core.luppi.intent import detect_intent
from core.luppi.conversational import compose_conversational
from core.luppi.emotional import analyze_emotion


class Command(BaseCommand):
    help = 'Test LUPPI with real failed conversation'

    def handle(self, *args, **options):
        test_messages = [
            "hii",
            "kaise ho aap",
            "main thik hun",
            "mera breakup ho gya hai",
            "main tut raha hun",
            "usko vapas kaise lekar aaun",
        ]
        
        self.stdout.write(self.style.SUCCESS("Testing real conversation that failed...\n"))
        
        for msg in test_messages:
            intent = detect_intent(msg)
            emotion = analyze_emotion(msg)
            reply = compose_conversational(intent, msg, emotion)
            
            self.stdout.write(f"User: {msg}")
            self.stdout.write(f"Intent: {intent.intent.value} (depth: {intent.depth.value})")
            self.stdout.write(f"LUPPI: {reply}")
            self.stdout.write("-" * 80)
