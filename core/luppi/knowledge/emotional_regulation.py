"""
Emotional Regulation knowledge for LUPPI 3.0.
"""
from .types import DomainKnowledge


EMOTIONAL_REGULATION_KNOWLEDGE = DomainKnowledge(
    name="emotional_regulation",
    description="Understanding and managing emotions effectively",
    principles=[
        "All emotions are valid and provide information",
        "Emotional regulation is about managing expression, not suppression",
        "Emotions have a natural lifecycle - they pass if allowed",
        "Regulation skills can be learned and practiced",
        "Different emotions require different regulation strategies",
    ],
    insights=[
        {
            "id": "emotional_regulation_1",
            "title": "The Purpose of Emotions",
            "body": "Emotions aren't random - they're information systems. Fear signals danger, anger signals violation, sadness signals loss, joy signals reward, anxiety signals uncertainty. Each emotion evolved to help you survive and thrive. The problem isn't having emotions - it's when emotions don't match the situation or when they're too intense to manage. Emotional regulation isn't about eliminating emotions - it's about understanding what they're telling you and responding appropriately. When you can identify the message in your emotion, you can make better decisions about what to do.",
        },
        {
            "id": "emotional_regulation_2",
            "title": "Suppression vs Regulation",
            "body": "Suppressing emotions means pushing them down, pretending they don't exist, distracting yourself from feeling. This might work temporarily but emotions don't go away - they go underground and often come back stronger. Regulation means experiencing the emotion but choosing how to express it. It's the difference between 'I'm not angry' (suppression) and 'I'm angry and I need to take a walk before I speak' (regulation). Suppression leads to emotional buildup, physical symptoms, and eventual explosion. Regulation leads to emotional balance, better relationships, and long-term wellbeing.",
        },
        {
            "id": "emotional_regulation_3",
            "title": "The 90-Second Rule",
            "body": "Neuroscientist Jill Bolte Taylor discovered that the chemical surge of an emotion lasts only 90 seconds in the body. After that, if you're still feeling the emotion, it's because you're re-triggering it with your thoughts. This is powerful knowledge: the intense physical sensation of anger, fear, or sadness is temporary. If you can stay with the sensation without feeding it with stories, it will pass. The practice: notice the emotion, feel it in your body, breathe through it, and don't engage the thoughts. After 90 seconds, the intensity will decrease. Then you can think clearly about what to do.",
        },
        {
            "id": "emotional_regulation_4",
            "title": "Grounding Techniques",
            "body": "When emotions feel overwhelming, grounding techniques help you return to the present moment. The 5-4-3-2-1 technique: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste. Body scan: notice sensations from your toes to your head. Deep breathing: 4 counts in, 4 counts hold, 4 counts out. These techniques work by shifting focus from internal emotional experience to external sensory experience. They don't solve the problem causing the emotion, but they create space so you can respond rather than react. Practice these when you're calm so they're available when you need them.",
        },
        {
            "id": "emotional_regulation_5",
            "title": "Emotional Granularity",
            "body": "Emotional granularity is the ability to identify specific emotions rather than broad categories. Instead of 'I feel bad,' you might feel 'disappointed, frustrated, and a bit ashamed.' Research shows that people with higher emotional granularity regulate emotions better. When you can name exactly what you're feeling, you can choose the right strategy. Disappointment might need acceptance, frustration might need problem-solving, shame might need self-compassion. The practice: expand your emotional vocabulary. Instead of just 'sad,' consider: lonely, grief, melancholy, heartbroken, disappointed. The more precise you can be, the better you can regulate.",
        },
    ],
)
