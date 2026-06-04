"""
Therapeutic techniques library for LUPPI 2.0.
Provides structured exercises for emotional regulation and mental health.
"""
from ..domains import Domain
from .types import DomainKnowledge, Insight

TECHNIQUES_KNOWLEDGE = DomainKnowledge(
    domain=Domain.GENERAL,
    principles=(
        'Techniques are tools, not cures.',
        'Consistency matters more than intensity.',
        'What works varies by individual.',
    ),
    insights=(
        Insight(
            'tech_grounding_01', Domain.GENERAL,
            ('ground', 'panic', 'anxiety', 'overwhelm', 'calm down'),
            '5-4-3-2-1 Grounding Technique:\n\n'
            '• 5 things you can SEE\n'
            '• 4 things you can TOUCH\n'
            '• 3 things you can HEAR\n'
            '• 2 things you can SMELL\n'
            '• 1 thing you can TASTE\n\n'
            'This pulls attention from internal chaos to external reality.',
            weight=1.2,
        ),
        Insight(
            'tech_breathing_01', Domain.GENERAL,
            ('breathe', 'breathing', 'calm', 'relax', 'anxiety'),
            '4-7-8 Breathing:\n\n'
            '• Inhale for 4 seconds\n'
            '• Hold for 7 seconds\n'
            '• Exhale for 8 seconds\n\n'
            'This activates parasympathetic nervous system, '
            'reducing heart rate and promoting calm.',
            weight=1.2,
        ),
        Insight(
            'tech_box_breathing_01', Domain.GENERAL,
            ('box breathing', 'stress', 'focus'),
            'Box Breathing (4-4-4-4):\n\n'
            '• Inhale for 4\n'
            '• Hold for 4\n'
            '• Exhale for 4\n'
            '• Hold empty for 4\n\n'
            'Used by Navy SEALs for stress management. '
            'Builds focus and emotional regulation.',
            weight=1.1,
        ),
        Insight(
            'tech_journaling_01', Domain.GENERAL,
            ('journal', 'write', 'express', 'thoughts'),
            'Brain Dump Journaling:\n\n'
            'Set timer for 5 minutes. Write everything in your mind '
            'without stopping, editing, or judging. '
            'When done, read it once, then destroy it.\n\n'
            'This externalizes racing thoughts and reduces mental load.',
            weight=1.1,
        ),
        Insight(
            'tech_body_scan_01', Domain.GENERAL,
            ('body', 'tension', 'relax', 'scan'),
            'Body Scan Meditation:\n\n'
            'Close eyes. Start at toes, move up slowly. '
            'Notice tension in each body part. '
            'Breathe into it, imagine it releasing.\n\n'
            'Reconnects mind with body, reduces stored stress.',
            weight=1.0,
        ),
        Insight(
            'tech_cbt_reframe_01', Domain.GENERAL,
            ('negative thought', 'reframe', 'cbt', 'challenge'),
            'CBT Thought Reframing:\n\n'
            '1. Identify the negative thought\n'
            '2. Ask: Is this absolutely true?\n'
            '3. What evidence supports it?\n'
            '4. What evidence contradicts it?\n'
            '5. What\'s a more balanced thought?\n\n'
            'This breaks automatic negative thinking patterns.',
            weight=1.15,
        ),
        Insight(
            'tech_worry_time_01', Domain.GENERAL,
            ('worry', 'overthink', 'anxiety', 'time'),
            'Scheduled Worry Time:\n\n'
            'Set 15 minutes daily for worrying. '
            'When worries come up outside this time, '
            'write them down and say "I\'ll worry about this at 4 PM."\n\n'
            'This contains anxiety instead of letting it spread.',
            weight=1.05,
        ),
        Insight(
            'tech_progressive_muscle_01', Domain.GENERAL,
            ('muscle', 'relax', 'tension', 'progressive'),
            'Progressive Muscle Relaxation:\n\n'
            'Tense each muscle group for 5 seconds, then release for 10. '
            'Start with toes, work up to head.\n\n'
            'Teaches body to recognize and release tension.',
            weight=1.0,
        ),
    ),
)
