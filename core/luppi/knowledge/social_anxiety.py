"""
Social Anxiety knowledge for LUPPI 3.0.
"""
from ..domains import Domain
from .types import DomainKnowledge, Insight


SOCIAL_ANXIETY_KNOWLEDGE = DomainKnowledge(
    domain=Domain.GENERAL,
    principles=(
        "Social anxiety is a fear of negative evaluation, not just shyness",
        "The fear is often disproportionate to the actual risk",
        "Avoidance maintains and strengthens anxiety",
        "Gradual exposure is the most effective treatment",
        "Social anxiety is highly treatable with the right approach",
    ),
    insights=(
        Insight(
            'social_anxiety_1', Domain.GENERAL,
            ('social', 'anxiety', 'fear', 'judge', 'nervous', 'public'),
            "Social anxiety isn't just about being shy - it's a specific fear of being judged, criticized, or rejected by others. This fear activates the same threat response as physical danger. Your brain perceives social situations as potentially life-threatening because in evolutionary terms, social rejection meant death. The fear isn't about the situation itself - it's about what you think might happen: people will think you're stupid, awkward, boring, or unlikeable. The key insight: the fear is about your imagination of what others think, not what they actually think.",
        ),
        Insight(
            'social_anxiety_2', Domain.GENERAL,
            ('spotlight', 'watch', 'center', 'attention', 'embarrass'),
            "People with social anxiety often feel like they're constantly being watched and judged - like they're on stage under a spotlight. This is called the spotlight effect. In reality, most people are focused on themselves, not you. They're thinking about their own performance, their own insecurities, their own day. Even when they do notice you, they're far less critical than you imagine. The spotlight feels real, but it's an illusion created by your anxious mind. Everyone has this to some degree, but social anxiety amplifies it dramatically.",
        ),
        Insight(
            'social_anxiety_3', Domain.GENERAL,
            ('avoid', 'escape', 'safety', 'behavior', 'cop'),
            "Social anxiety leads to safety behaviors - things you do to reduce anxiety in the moment: avoiding eye contact, rehearsing conversations excessively, staying quiet, leaving early, using alcohol to cope. These behaviors provide temporary relief but actually maintain the anxiety long-term. They prevent you from learning that the feared outcome doesn't happen. Avoidance is the biggest enemy in social anxiety - every time you avoid, you reinforce the belief that the situation is dangerous. The path forward involves gradually reducing safety behaviors and facing feared situations.",
        ),
        Insight(
            'social_anxiety_4', Domain.GENERAL,
            ('exposure', 'gradual', 'face', 'practice', 'step'),
            "The most effective treatment for social anxiety is gradual exposure - systematically facing feared situations in small steps. Start with situations that cause mild anxiety, not overwhelming terror. As you stay in the situation and nothing bad happens, your brain learns that it's safe. Gradually increase the difficulty. The key principles: stay in the situation until anxiety decreases (don't escape), don't use safety behaviors, repeat the situation until it becomes boring, and celebrate small wins. Exposure isn't about forcing yourself - it's about teaching your brain through experience that social situations are safe.",
        ),
        Insight(
            'social_anxiety_5', Domain.GENERAL,
            ('thought', 'cognitive', 'restructure', 'evidence', 'realistic'),
            "Social anxiety is fueled by distorted thoughts: 'Everyone will notice my mistake', 'They'll think I'm incompetent', 'I'll humiliate myself'. These thoughts feel true but aren't based on evidence. Cognitive restructuring involves: identifying the anxious thought, examining the evidence for and against it, considering alternative explanations, and developing a more balanced thought. For example, instead of 'Everyone will notice I'm nervous', try 'Some people might notice I'm nervous, but most won't care, and nervousness is normal.' The goal isn't positive thinking - it's realistic thinking.",
        ),
    ),
)
