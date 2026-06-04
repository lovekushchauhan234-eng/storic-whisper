"""
Comprehensive stress test for LUPPI 3.0 with multi-turn conversations.
Tests multiple psychological scenarios with realistic user behavior.
"""
from django.core.management.base import BaseCommand
from django.test import RequestFactory
from core.luppi import chat


class SimpleSession:
    """Simple session mock for testing."""
    def __init__(self):
        self.session_key = 'test_session_key'
        self.modified = False
        self._data = {}
    
    def get(self, key, default=None):
        return self._data.get(key, default)
    
    def __setitem__(self, key, value):
        self._data[key] = value


class Command(BaseCommand):
    help = 'Run comprehensive stress test on LUPPI with multi-turn conversations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--scenario',
            type=str,
            help='Specific scenario to test (breakup, dependency, validation, anxiety, self_esteem, behavior, stoicism, dark_psychology, all)'
        )
        parser.add_argument(
            '--turns',
            type=int,
            default=3,
            help='Number of conversation turns per scenario'
        )

    def handle(self, *args, **options):
        scenario = options.get('scenario', 'all')
        turns = options.get('turns', 3)

        self.stdout.write(self.style.SUCCESS('=== LUPPI 3.0 Comprehensive Stress Test ===\n'))

        scenarios = self.get_scenarios()

        if scenario != 'all' and scenario in scenarios:
            self.run_scenario(scenario, scenarios[scenario], turns)
        elif scenario == 'all':
            for name, messages in scenarios.items():
                self.run_scenario(name, messages, turns)
        else:
            self.stdout.write(self.style.ERROR(f'Unknown scenario: {scenario}'))

        self.stdout.write(self.style.SUCCESS('\n=== Stress Test Complete ==='))

    def get_scenarios(self):
        """Define test scenarios with multi-turn conversations."""
        return {
            'breakup': [
                "Mera breakup ho gaya hai, vo mujhe chhod kar chali gayi, dil bohot ro raha hai aur chain nahi aa raha... kya karu?",
                "Kyun mujhe hua aisa? Main kya galat kiya tha?",
                "Kab tak yeh dard rahega? Main kab theek hoga?",
                "Kya use wapas lane ka koi tarika hai?",
                "Mujhe lag raha hai main kabhi khush nahi hoga"
            ],
            'dependency': [
                "Main bina uske soch nahi paata, har waqt uski hi baatein dimaag mein rehti hain",
                "Jab vo call nahi karti, mujhe darr lagta hai ki vo mujhe chhod degi",
                "Main apne friends se bhi door ho gaya hoon sirf uski wajah se",
                "Kya yeh pyaar hai ya obsession? Main confuse hoon",
                "Mujhe apni aazadi wapas chahiye par main usse chhod nahi paata"
            ],
            'validation': [
                "Kya main kaam ka hoon? Kisi ko meri parvah nahi hai",
                "Log mujhe ignore karte hain, main unimportant lagta hoon",
                "Mere parents bhi mujhe appreciate nahi karte",
                "Social media dekh kar mujhe inferiority complex ho jata hai",
                "Kya main kabhi confident ban paunga?"
            ],
            'anxiety': [
                "Mera future ka bahut darr hai, kya hoga mujhe?",
                "Meri job ka tension hai, main fail ho jaaunga",
                "Mere parents ki health ka darr hai, unhe kuch ho gaya toh?",
                "Raat ko sone se pehle bahut zyada sochta hoon",
                "Mera dil bahut tez dhadakta hai, panic attack aate hain"
            ],
            'self_esteem': [
                "Main kaun hoon? Main kuch bhi achieve nahi kar paaya",
                "Mere sabhi friends successful hain, main hi fail hoon",
                "Main khud se nafrat karta hoon",
                "Mere paas koi talent nahi hai",
                "Kya main kabhi kuch bada kar paunga?"
            ],
            'behavior': [
                "Log aise kyun behave karte hain jo hurt kare?",
                "Kuch log fake hote hain, pehle ache phir badal jaate hain",
                "Kya human nature hi aisi hai selfish?",
                "Trust karna mushkil hai logon mein",
                "Kya sachche log bhi exist karte hain?"
            ],
            'stoicism': [
                "Stoicism kya hota hai? Kaise apply karu life mein?",
                "Emotions ko control kaise karein?",
                "Bad situations mein kaise calm rahein?",
                "Pain ko kaise handle karein stoic way mein?",
                "Seneca ya Marcus Aurelius ke kya important lessons hain?"
            ],
            'dark_psychology': [
                "Kya manipulation kya hota hai? Kaise recognize karein?",
                "Gaslighting kya hai? Kaise pata chalega?",
                "Narcissists kaise behave karte hain?",
                "Toxic relationships kaise identify karein?",
                "Apne aap ko kaise protect karein dark psychology se?"
            ]
        }

    def run_scenario(self, name, messages, max_turns):
        """Run a single scenario with multiple turns."""
        self.stdout.write(self.style.WARNING(f'\n--- Scenario: {name.upper()} ---\n'))

        factory = RequestFactory()
        request = factory.get('/')
        request.session = SimpleSession()
        request.user = type('User', (), {'is_authenticated': False})()

        conversation_log = []

        for i, message in enumerate(messages[:max_turns], 1):
            try:
                self.stdout.write(f'Turn {i}:')
                self.stdout.write(f'  User: {message}')
                
                response = chat(request, message)
                
                self.stdout.write(f'  LUPPI: {response.reply[:200]}...')
                self.stdout.write(f'  Domain: {response.domain}')
                self.stdout.write(f'  Emotion: {response.emotion}')
                self.stdout.write(f'  Confidence: {response.confidence}')
                self.stdout.write(f'  Provider: {response.provider}')
                
                conversation_log.append({
                    'turn': i,
                    'user_message': message,
                    'luppi_response': response.reply[:200],
                    'domain': response.domain,
                    'emotion': response.emotion,
                    'confidence': response.confidence,
                    'provider': response.provider,
                })
                
                self.stdout.write('')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ERROR: {str(e)}'))
                conversation_log.append({
                    'turn': i,
                    'user_message': message,
                    'error': str(e),
                })
                self.stdout.write('')

        self.stdout.write(self.style.SUCCESS(f'--- {name} Complete ---\n'))
