"""
Meaning & Purpose knowledge for LUPPI 3.0.
"""
from .types import DomainKnowledge


MEANING_KNOWLEDGE = DomainKnowledge(
    name="meaning",
    description="Finding and creating meaning in life",
    principles=[
        "Meaning is created, not found",
        "Meaning can exist even in suffering",
        "Purpose is about contribution, not achievement",
        "Meaning changes throughout life",
        "Small acts of meaning matter as much as grand purposes",
    ],
    insights=[
        {
            "id": "meaning_1",
            "title": "Meaning vs Happiness",
            "body": "Happiness is a feeling state - pleasure, satisfaction, joy. Meaning is about significance - feeling that your life matters, that you're connected to something larger. Research shows that pursuing meaning often leads to long-term wellbeing, while pursuing happiness alone can be unsatisfying. Meaning can exist even in pain and difficulty - think of people who find meaning in caring for a sick family member or working through a challenge. Happiness comes and goes, but meaning provides stability and direction. The key insight: you don't need to be happy to have a meaningful life.",
        },
        {
            "id": "meaning_2",
            "title": "Sources of Meaning",
            "body": "Meaning comes from multiple sources, not just one: Relationships - loving and being loved, contributing to others' lives. Work or creative pursuits - using your skills to create something valuable. Values and causes - standing for something that matters to you. Personal growth - becoming the person you want to be. Experiences - engaging with life fully, both joys and challenges. Legacy - what you leave behind. The problem comes when you expect all your meaning from one source, like work or a relationship. Diversify your meaning portfolio so if one area struggles, others can sustain you.",
        },
        {
            "id": "meaning_3",
            "title": "Creating Meaning in Difficult Times",
            "body": "Viktor Frankl, a psychiatrist who survived Nazi concentration camps, wrote that meaning can be found even in the worst suffering. He observed that those who found meaning - in helping others, in holding onto hope, in refusing to be broken - were more likely to survive. When life feels meaningless, you can create meaning through: choosing your attitude toward your situation, finding small ways to help others, setting meaningful goals even in difficult circumstances, connecting to values that matter to you, and recognizing that your struggle might eventually help others. Meaning isn't about the situation being good - it's about your relationship to it.",
        },
        {
            "id": "meaning_4",
            "title": "Purpose vs Achievement",
            "body": "Purpose is often confused with achievement, but they're different. Achievement is about reaching goals - getting the promotion, finishing the project, hitting a milestone. Purpose is about direction and contribution - why you're doing what you're doing. You can achieve without purpose (checking boxes without caring), and you can have purpose without constant achievement (raising children with intention, living according to values). The pressure to constantly achieve can actually obscure purpose. When you're always chasing the next goal, you never pause to ask why. Purpose provides meaning in the journey, not just the destination.",
        },
        {
            "id": "meaning_5",
            "title": "Small Acts of Meaning",
            "body": "Meaning doesn't require grand purposes or world-changing impact. Small daily acts create meaning: being kind to a stranger, doing work you care about, being present with loved ones, standing by your values in small choices, taking care of yourself, learning something new. These small acts accumulate into a meaningful life. The problem is we often dismiss them as not 'real' meaning because they're not dramatic enough. But meaning is built in the mundane, not just the extraordinary. If you're waiting for a grand purpose to appear, you might miss the meaning that's available right now in your daily choices.",
        },
    ],
)
