from django.test import Client, TestCase

from core.luppi import chat as luppi_chat
from core.luppi.classifier import classify_domain
from core.luppi.domains import Domain
from core.luppi.emotional import EmotionalTone, analyze_emotion
from core.luppi.intent import ConversationIntent, ResponseDepth, detect_intent
from core.luppi.retrieval import retrieve_insight


class LuppiIntentTests(TestCase):
    def test_greeting(self):
        r = detect_intent('Hi')
        self.assertEqual(r.intent, ConversationIntent.GREETING)
        self.assertEqual(r.depth, ResponseDepth.NONE)

    def test_how_are_you(self):
        r = detect_intent('How are you?')
        self.assertEqual(r.intent, ConversationIntent.SMALL_TALK)

    def test_study_context(self):
        r = detect_intent('I feel distracted while studying')
        self.assertEqual(r.intent, ConversationIntent.STUDY_FOCUS)

    def test_relationship_hurt(self):
        r = detect_intent('My relationship is hurting me')
        self.assertEqual(r.intent, ConversationIntent.RELATIONSHIP)


class LuppiClassifierTests(TestCase):
    def test_breakup_domain(self):
        r = classify_domain('breakup ke baad no contact karna chahiye?')
        self.assertEqual(r.domain, Domain.BREAKUP)

    def test_dopamine_domain(self):
        r = classify_domain('reels scroll addiction dopamine')
        self.assertEqual(r.domain, Domain.DOPAMINE)


class LuppiEmotionTests(TestCase):
    def test_grief_detection(self):
        e = analyze_emotion('bahut dard ho raha hai, ro raha hoon')
        self.assertEqual(e.primary, EmotionalTone.GRIEF)


class LuppiRetrievalTests(TestCase):
    def test_insight_on_topic(self):
        r = retrieve_insight('gaslighting', Domain.DARK, exclude_ids=[])
        self.assertIsNotNone(r)
        self.assertTrue(r.is_relevant)

    def test_no_random_insight(self):
        r = retrieve_insight('hi', Domain.BREAKUP, exclude_ids=[])
        self.assertIsNone(r)


class LuppiApiTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_chat_requires_post(self):
        r = self.client.get('/ai-saathi/chat/')
        self.assertEqual(r.status_code, 405)

    def test_greeting_short(self):
        r = self.client.post(
            '/ai-saathi/chat/',
            data='{"message": "Hi"}',
            content_type='application/json',
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['meta']['intent'], 'greeting')
        self.assertLess(len(data['reply']), 200)

    def test_study_natural(self):
        r = self.client.post(
            '/ai-saathi/chat/',
            data='{"message": "I feel distracted while studying"}',
            content_type='application/json',
        )
        data = r.json()
        self.assertEqual(data['meta']['intent'], 'study_focus')
        reply_lower = data['reply'].lower()
        self.assertTrue(
            'padh' in reply_lower or 'focus' in reply_lower or 'distract' in reply_lower or 'exam' in reply_lower
        )

    def test_breakup_deep(self):
        r = self.client.post(
            '/ai-saathi/chat/',
            data='{"message": "breakup ke baad no contact kyun important hai?"}',
            content_type='application/json',
        )
        data = r.json()
        self.assertIn(data['meta']['intent'], ('relationship', 'deep_psychology'))
        self.assertTrue(len(data['reply']) > 30)
