"""
100-Question Stress Test for LUPPI Intent Routing
Tests greetings, relationship pain, psychological concepts, and emotional distress.
"""
from django.core.management.base import BaseCommand
from django.http import HttpRequest
from core.luppi import chat


class Command(BaseCommand):
    help = 'Run 100-question stress test on LUPPI intent routing'

    def handle(self, *args, **options):
        # 100-question test database
        test_cases = {
            'greetings': [
                "hi", "hello", "hey", "hii", "namaste", "नमस्ते", "kaise ho", "kaise ho aap",
                "how are you", "how r u", "kya haal", "what's up", "sup", "good morning",
                "good night", "gm", "gn", "main thik hun", "mein theek hoon", "i'm fine",
            ],
            'relationship_pain': [
                "gf chhod gai", "girlfriend left me", "breakup ho gaya", "mera breakup ho gya hai",
                "usko wapas kaise laun", "how to get her back", "usko vapas kaise lekar aaun",
                "main tut raha hun", "i'm broken", "dil toot gaya", "heartbroken",
                "woh mujhe chhod kar chali gayi", "she left me", "relationship khatam ho gaya",
                "ladki ne dhoka diya", "she cheated on me", "cheat hui hai",
                "pyaar mein dhoka", "love betrayal", "emotional pain",
                "akela feel kar raha hoon", "lonely after breakup", "alone without her",
                "miss her so much", "uski yaad aa rahi hai", "can't forget her",
                "kab theek hoga", "when will i heal", "healing process",
                "kya main galat tha", "was it my fault", "blame myself",
                "kyun hua aisa", "why did this happen", "reason for breakup",
                "kaise move on karun", "how to move on", "forget her",
                "relationship advice", "love problem", "dating issues",
                "ladki kaise pataye", "how to impress girl", "dating tips",
                "new relationship", "start over", "fresh start",
                "trust issues", "can't trust again", "trust broken",
                "emotional attachment", "attached to her", "letting go",
                "closure chahiye", "need closure", "why she left",
                "rebound relationship", "moving on quickly", "dating again",
                "ex girlfriend", "my ex", "past relationship",
            ],
            'psychological_concepts': [
                "stoicism kya hai", "what is stoicism", "stoic philosophy",
                "manipulation kya hai", "what is manipulation", "manipulative behavior",
                "gaslighting kya hai", "what is gaslighting", "gaslighting signs",
                "narcissist kya hai", "what is narcissist", "narcissistic personality",
                "toxic relationship", "toxic partner", "toxic behavior",
                "emotional intelligence", "eq", "emotional awareness",
                "coping mechanisms", "how to cope", "coping strategies",
                "anxiety kya hai", "what is anxiety", "anxiety symptoms",
                "depression kya hai", "what is depression", "depression signs",
                "self esteem", "confidence", "self worth",
                "attachment theory", "attachment styles", "secure attachment",
                "cognitive behavioral therapy", "cbt", "therapy techniques",
                "mindfulness", "meditation", "being present",
                "boundaries kya hai", "what are boundaries", "setting boundaries",
                "emotional dependency", "codependency", "emotional independence",
                "trigger kya hai", "what is trigger", "emotional triggers",
                "trauma kya hai", "what is trauma", "trauma response",
            ],
            'emotional_distress': [
                "mujhe pain ho raha hai", "i'm in pain", "bahut dard ho raha hai",
                "akelepan lag raha hai", "feeling lonely", "loneliness",
                "stress ho raha hai", "stressed out", "too much stress",
                "tension hai", "tension", "anxious feeling",
                "depressed feel kar raha hoon", "feeling depressed", "depression",
                "suicidal thoughts", "want to die", "life not worth living",
                "overthinking kar raha hoon", "overthinking", "can't stop thinking",
                "sleep nahi aa rahi", "insomnia", "can't sleep",
                "appetite kam ho gaya", "not eating", "loss of appetite",
                "energy nahi hai", "no energy", "feeling tired",
                "motivation nahi hai", "no motivation", "unmotivated",
                "confused hoon", "feeling confused", "don't know what to do",
                "angry hoon", "feeling angry", "rage",
                "sad feel kar raha hoon", "feeling sad", "sadness",
                "fear lag raha hai", "feeling scared", "fear",
                "guilt feel kar raha hoon", "feeling guilty", "guilt",
                "shame feel kar raha hoon", "feeling ashamed", "shame",
                "hopeless feel kar raha hoon", "feeling hopeless", "hopelessness",
                "overwhelmed feel kar raha hoon", "feeling overwhelmed", "overwhelmed",
                "empty feel kar raha hoon", "feeling empty", "emptiness",
                "worthless feel kar raha hoon", "feeling worthless", "worthlessness",
                "panic attack", "panic", "anxiety attack",
                "crying bahut ho raha hai", "can't stop crying", "tears",
                "emotional breakdown", "breakdown", "mental breakdown",
                "burnout", "exhausted", "burned out",
                "grief", "mourning", "loss",
            ],
        }

        # Create mock request with proper session
        from django.contrib.sessions.backends.db import SessionStore
        
        class MockRequest:
            def __init__(self):
                self.session = SessionStore()
                self.session_key = self.session.session_key
                self.META = {'REMOTE_ADDR': '127.0.0.1'}
        
        request = MockRequest()
        
        total_tests = 0
        passed_tests = 0
        failed_tests = []
        
        # Forbidden responses (robotic fallbacks)
        forbidden_responses = [
            "Yeh topic hai 😊",
            "यह एक बहुत ही important topic है",
            "Interesting point",
            "Yeh complex issue hai",
        ]
        
        self.stdout.write(self.style.SUCCESS("Starting 100-Question Stress Test...\n"))
        
        for category, messages in test_cases.items():
            self.stdout.write(f"\nTesting {category.upper()} ({len(messages)} tests):")
            
            for msg in messages:
                total_tests += 1
                try:
                    response = chat(request, msg)
                    reply = response.reply
                    
                    # Check if response contains forbidden robotic strings
                    is_forbidden = any(forbidden in reply for forbidden in forbidden_responses)
                    
                    # Category-specific validation
                    if category == 'greetings':
                        # Greetings should NOT get robotic "Yeh topic hai" responses
                        if is_forbidden:
                            failed_tests.append({
                                'category': category,
                                'message': msg,
                                'reply': reply,
                                'reason': 'Greeting got robotic fallback'
                            })
                            self.stdout.write(self.style.ERROR(f"  FAIL: {msg} -> {reply[:50]}..."))
                        else:
                            passed_tests += 1
                            self.stdout.write(self.style.SUCCESS(f"  PASS: {msg}"))
                    
                    elif category == 'relationship_pain':
                        # Relationship pain should get empathetic responses, NOT robotic
                        if is_forbidden or len(reply) < 20:
                            failed_tests.append({
                                'category': category,
                                'message': msg,
                                'reply': reply,
                                'reason': 'Relationship pain got robotic/short response'
                            })
                            self.stdout.write(self.style.ERROR(f"  FAIL: {msg} -> {reply[:50]}..."))
                        else:
                            passed_tests += 1
                            self.stdout.write(self.style.SUCCESS(f"  PASS: {msg}"))
                    
                    elif category == 'psychological_concepts':
                        # Concepts should get informative responses
                        if is_forbidden or len(reply) < 30:
                            failed_tests.append({
                                'category': category,
                                'message': msg,
                                'reply': reply,
                                'reason': 'Concept got robotic/short response'
                            })
                            self.stdout.write(self.style.ERROR(f"  FAIL: {msg} -> {reply[:50]}..."))
                        else:
                            passed_tests += 1
                            self.stdout.write(self.style.SUCCESS(f"  PASS: {msg}"))
                    
                    elif category == 'emotional_distress':
                        # Emotional distress should get supportive responses
                        if is_forbidden or len(reply) < 20:
                            failed_tests.append({
                                'category': category,
                                'message': msg,
                                'reply': reply,
                                'reason': 'Emotional distress got robotic/short response'
                            })
                            self.stdout.write(self.style.ERROR(f"  FAIL: {msg} -> {reply[:50]}..."))
                        else:
                            passed_tests += 1
                            self.stdout.write(self.style.SUCCESS(f"  PASS: {msg}"))
                
                except Exception as e:
                    failed_tests.append({
                        'category': category,
                        'message': msg,
                        'reply': str(e),
                        'reason': 'Exception occurred'
                    })
                    self.stdout.write(self.style.ERROR(f"  ERROR: {msg} -> {str(e)}"))
        
        # Summary
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS(f"\nTEST SUMMARY"))
        self.stdout.write(f"Total Tests: {total_tests}")
        self.stdout.write(f"Passed: {passed_tests}")
        self.stdout.write(f"Failed: {len(failed_tests)}")
        self.stdout.write(f"Pass Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests:
            self.stdout.write("\n" + self.style.ERROR("FAILED TESTS:"))
            for fail in failed_tests[:10]:  # Show first 10 failures
                self.stdout.write(f"\nCategory: {fail['category']}")
                self.stdout.write(f"Message: {fail['message']}")
                self.stdout.write(f"Reason: {fail['reason']}")
                self.stdout.write(f"Reply: {fail['reply'][:100]}...")
        
        if passed_tests == total_tests:
            self.stdout.write("\n" + self.style.SUCCESS("✅ ALL TESTS PASSED (100/100)"))
        else:
            self.stdout.write("\n" + self.style.ERROR(f"❌ {len(failed_tests)} TESTS FAILED"))
