"""
Real Human Conversation Audit - Simulate 200+ real user conversations
Tests greetings, casual chat, dating, relationship support, loneliness, study, psychology concepts
"""
from django.core.management.base import BaseCommand
from django.contrib.sessions.backends.db import SessionStore
from core.luppi import chat


class Command(BaseCommand):
    help = 'Run real human conversation audit to detect robotic/AI-sounding responses'

    def handle(self, *args, **options):
        # 200+ real user conversation test cases
        test_cases = {
            'greetings': [
                "hi", "hello", "hey", "hii", "namaste", "नमस्ते", "kaise ho", "kaise ho aap",
                "how are you", "how r u", "kya haal", "what's up", "sup", "good morning",
                "good night", "gm", "gn", "main thik hun", "mein theek hoon", "i'm fine",
                "yo", "wassup", "hola", "hey there", "hello ji", "namaskar", "pranam",
            ],
            'casual_chat': [
                "kya kar rahe ho", "what doing", "kya chal raha hai", "what's up",
                "bored hoon", "feeling bored", "kuch kaam nahi hai", "free hoon",
                "mujhe akela lag raha hai", "feeling lonely", "kisi se baat karni hai",
                "tum kya ho", "tum kaun ho", "tumhara naam kya hai", "about you",
                "tumse dosti kar sakte hain", "can we be friends", "friendship karoge",
            ],
            'dating_questions': [
                "ladki kaise pataye", "how to impress girl", "dating tips kya hai",
                "first date par kya karein", "approach kaise karein", "girlfriend kaise banaye",
                "ladki patane ke tarike", "impress kaise karein", "kaise pataye",
                "dating advice chahiye", "relationship tips", "love guru bano",
            ],
            'relationship_advice': [
                "relationship kaise theek karein", "love problem hai", "pyaar mein pareshani",
                "relationship advice chahiye", "couple goals kaise banein", "long distance relationship",
                "relationship mein trust kaise layein", "love life theek karni hai",
                "partner ko kaise samjhein", "relationship fights kaise khatam karein",
            ],
            'breakup_support': [
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
            ],
            'loneliness': [
                "akela feel kar raha hoon", "feeling lonely", "loneliness",
                "mujhe kisi ki zarurat hai", "need someone", "koi nahi hai mere paas",
                "crowd mein bhi akela", "alone in crowd", "social isolation",
                "friends nahi hain", "no friends", "friend circle nahi hai",
                "family se door", "away from family", "home sick",
            ],
            'overthinking': [
                "overthinking kar raha hoon", "overthinking", "can't stop thinking",
                "dimag ghoom raha hai", "mind racing", "thoughts not stopping",
                "sab soch raha hoon", "thinking too much", "analysis paralysis",
                "future ke baare mein soch raha hoon", "worrying about future", "anxious thoughts",
                "past ki baatein yaad aa rahi hain", "past memories", "can't let go",
            ],
            'study_problems': [
                "padhai mein focus nahi kar pa raha", "can't focus on studies", "study distraction",
                "exam ka stress hai", "exam stress", "pressure of exams",
                "procrastination kar raha hoon", "procrastinating", "delaying work",
                "motivation nahi hai padhai ki", "no motivation to study", "don't feel like studying",
                "career confuse hoon", "confused about career", "what to do in life",
                "concentration nahi hai", "lack of concentration", "can't concentrate",
                "phone addiction hai", "addicted to phone", "reels addiction",
                "brain fog hai", "mental fog", "can't think clearly",
            ],
            'motivation': [
                "motivation chahiye", "need motivation", "demotivated feel kar raha hoon",
                "life mein interest nahi hai", "no interest in life", "bored with life",
                "kuch achieve karna hai", "want to achieve something", "goals in life",
                "success kaise milegi", "how to be successful", "want to succeed",
                "self improvement karna hai", "want to improve myself", "personal growth",
                "confidence boost chahiye", "need confidence", "low self esteem",
            ],
            'psychology_concepts': [
                "gaslighting kya hai", "what is gaslighting", "gaslighting signs",
                "narcissist kya hota hai", "what is narcissist", "narcissistic personality",
                "secure attachment", "attachment theory", "attachment styles",
                "cbt kya hai", "what is cbt", "cognitive behavioral therapy",
                "emotional intelligence", "eq", "emotional awareness",
                "coping mechanisms", "coping strategies", "how to cope",
                "trauma kya hai", "what is trauma", "trauma response",
                "boundaries kya hote hain", "what are boundaries", "setting boundaries",
                "codependency", "toxic relationship", "toxic partner",
                "stoicism", "mindfulness", "meditation", "being present",
                "self esteem", "self worth", "confidence",
                "manipulation", "toxic behavior", "emotional abuse",
            ],
            'emotional_support': [
                "mujhe pain ho raha hai", "i'm in pain", "bahut dard ho raha hai",
                "stress ho raha hai", "stressed out", "too much stress",
                "tension hai", "tension", "anxious feeling",
                "depressed feel kar raha hoon", "feeling depressed", "depression",
                "suicidal thoughts", "want to die", "life not worth living",
                "panic attack", "anxiety attack", "can't breathe",
                "sleep nahi aa rahi", "insomnia", "can't sleep",
                "appetite kam ho gaya", "not eating", "loss of appetite",
                "energy nahi hai", "no energy", "feeling tired",
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
                "emotional breakdown", "breakdown", "mental breakdown",
                "burnout", "exhausted", "burned out",
                "grief", "mourning", "loss",
            ],
        }

        # Create mock request
        class MockRequest:
            def __init__(self):
                self.session = SessionStore()
                self.session_key = self.session.session_key
                self.META = {'REMOTE_ADDR': '127.0.0.1'}

        request = MockRequest()

        # Robotic/AI-sounding patterns to detect
        robotic_patterns = [
            "Yeh topic hai 😊",
            "यह एक बहुत ही important topic है",
            "Interesting point",
            "Yeh complex issue hai",
            "Achha laga tum aaye",
            "Main yahin hoon",
            "Achha sawal hai 😊",
            "Hmm, achha 😊",
            "Yeh ek important psychological concept hai 😊",
            "Good question! 😊",
            "Yeh interesting hai 😊",
            "सुन रहा हूँ — बताओ थोड़ा और 😊",
            "यहाँ हूँ। एक line में बताओ — क्या चल रहा है?",
            "I'm listening. What's on your mind?",
        ]

        total_tests = 0
        robotic_responses = []
        repetitive_responses = {}
        response_variety = {}

        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('REAL HUMAN CONVERSATION AUDIT'))
        self.stdout.write(self.style.SUCCESS('=' * 80))

        for category, messages in test_cases.items():
            self.stdout.write(f"\n{self.style.WARNING(f'Testing {category.upper()} ({len(messages)} tests):')}")
            
            for message in messages:
                total_tests += 1
                response = chat(request, message, provider='local')
                reply = response.reply
                
                # Check for robotic patterns
                for pattern in robotic_patterns:
                    if pattern in reply:
                        robotic_responses.append({
                            'category': category,
                            'message': message,
                            'reply': reply,
                            'pattern': pattern
                        })
                        break
                
                # Track response variety
                if reply not in response_variety:
                    response_variety[reply] = []
                response_variety[reply].append((category, message))

        # Summary
        self.stdout.write(f'\n{self.style.SUCCESS("=" * 80)}')
        self.stdout.write(f'{self.style.SUCCESS("AUDIT SUMMARY")}')
        self.stdout.write(f'{self.style.SUCCESS("=" * 80)}')
        self.stdout.write(f'\nTotal Tests: {total_tests}')
        self.stdout.write(f'Robotic Responses Found: {len(robotic_responses)}')
        self.stdout.write(f'Unique Responses: {len(response_variety)}')
        
        if robotic_responses:
            self.stdout.write(f'\n{self.style.ERROR("ROBOTIC RESPONSES DETECTED:")}')
            for item in robotic_responses[:20]:  # Show first 20
                self.stdout.write(f'\n{self.style.WARNING("Category: " + item["category"])}')
                self.stdout.write(f'{self.style.WARNING("Message: " + item["message"])}')
                self.stdout.write(f'{self.style.ERROR("Pattern: " + item["pattern"])}')
                self.stdout.write(f'{self.style.ERROR("Reply: " + item["reply"][:100] + "...")}')
        
        # Check for repetitive responses
        repetitive = {k: v for k, v in response_variety.items() if len(v) > 3}
        if repetitive:
            self.stdout.write(f'\n{self.style.ERROR("REPETITIVE RESPONSES (used 3+ times):")}')
            for reply, contexts in sorted(repetitive.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
                self.stdout.write(f'\n{self.style.WARNING(f"Used {len(contexts)} times:")}')
                self.stdout.write(f'{self.style.ERROR(f"Reply: {reply[:80]}...")}')
        
        self.stdout.write(f'\n{self.style.SUCCESS("=" * 80)}')
