"""
Test LUPPI conversational quality improvements.
"""
from django.core.management.base import BaseCommand
from core.luppi.intent import detect_intent
from core.luppi.conversational import compose_conversational
from core.luppi.emotional import analyze_emotion


class Command(BaseCommand):
    help = 'Test LUPPI conversational responses'

    def handle(self, *args, **options):
        test_messages = [
            # Greetings
            "hello",
            "hi",
            "hey",
            "namaste",
            "good morning",
            "good night",
            
            # Small talk - how are you
            "kaise ho",
            "how are you",
            "kya haal hai",
            "what's up",
            
            # Small talk - what doing
            "kya kar rahe ho",
            "what doing",
            "kya chal raha hai",
            
            # Small talk - thanks
            "thanks",
            "shukriya",
            "thank you",
            
            # Small talk - bye
            "bye",
            "goodbye",
            "see you",
            
            # Dating/relationship casual
            "ladki kaise patayen",
            "kaise pataye",
            "impress kaise kare",
            "girlfriend kaise banaye",
            "dating tips",
            "first date",
            
            # Personal questions
            "tum kya ho",
            "tum kaun ho",
            "tumhara naam kya hai",
            "tumhare baare mein batao",
            "about you",
            
            # Casual conversation
            "hmm",
            "ok",
            "nice",
            "cool",
            "interesting",
            
            # Mixed casual
            "batao",
            "sun rahe ho",
            "achha",
            "theek hai",
            
            # Short messages
            "hi there",
            "hey you",
            "yo",
            "sup",
            
            # Hindi casual
            "arrey",
            "acha",
            "theek",
            "haan",
            
            # More greetings
            "hii",
            "helo",
            "gm",
            "gn",
            
            # More small talk
            "how r u",
            "wyd",
            "okay",
            "cool",
            "nice to meet you",
        ]
        
        self.stdout.write(self.style.SUCCESS(f"Testing {len(test_messages)} conversational messages...\n"))
        
        results = []
        for msg in test_messages:
            intent = detect_intent(msg)
            emotion = analyze_emotion(msg)
            reply = compose_conversational(intent, msg, emotion)
            
            results.append({
                'message': msg,
                'intent': intent.intent.value,
                'depth': intent.depth.value,
                'reply': reply,
            })
            
            self.stdout.write(f"Message: {msg}")
            self.stdout.write(f"Intent: {intent.intent.value} (depth: {intent.depth.value})")
            self.stdout.write(f"Reply: {reply[:100]}...")
            self.stdout.write("-" * 80)
        
        # Summary
        self.stdout.write(self.style.SUCCESS("\n=== SUMMARY ==="))
        intent_counts = {}
        for r in results:
            intent_counts[r['intent']] = intent_counts.get(r['intent'], 0) + 1
        
        for intent, count in intent_counts.items():
            self.stdout.write(f"{intent}: {count}")
        
        self.stdout.write(self.style.SUCCESS(f"\nTotal messages tested: {len(test_messages)}"))
