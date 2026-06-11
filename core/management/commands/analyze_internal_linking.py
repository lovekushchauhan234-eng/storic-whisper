from django.core.management.base import BaseCommand
from core.models import Article
from bs4 import BeautifulSoup
from django.conf import settings
import os
import sys
import dj_database_url


class Command(BaseCommand):
    help = 'Analyze published articles and identify missing semantic connections for internal linking'

    def add_arguments(self, parser):
        parser.add_argument('--database-url', type=str,
                            help='Temporary override DATABASE_URL for this run (e.g., production database)')

    def handle(self, *args, **options):
        # Handle database URL override
        original_database_url = os.environ.get('DATABASE_URL', '')
        if options['database_url']:
            os.environ['DATABASE_URL'] = options['database_url']
            # Reconfigure database connection
            settings.DATABASES['default'] = dj_database_url.parse(
                options['database_url'],
                conn_max_age=600,
                conn_health_checks=True,
            )
        self.stdout.write(self.style.SUCCESS('=== INTERNAL LINKING ANALYSIS ==='))
        self.stdout.write('')
        
        # Diagnostic output
        self.stdout.write(self.style.WARNING('=== COMMAND FILE INFO ==='))
        self.stdout.write(f'Command file path: {__file__}')
        self.stdout.write('')
        
        self.stdout.write(self.style.WARNING('=== ENVIRONMENT INFO ==='))
        self.stdout.write(f'Settings module: {settings.SETTINGS_MODULE}')
        self.stdout.write(f'Current working directory: {os.getcwd()}')
        self.stdout.write(f'Database engine: {settings.DATABASES["default"]["ENGINE"]}')
        self.stdout.write(f'Database name: {settings.DATABASES["default"]["NAME"]}')
        
        # Query all published articles
        articles = Article.objects.filter(is_published=True)
        total_articles = articles.count()
        
        self.stdout.write(f'Total published articles: {total_articles}')
        self.stdout.write('')
        
        # Restore original DATABASE_URL if it was overridden
        if options['database_url']:
            if original_database_url:
                os.environ['DATABASE_URL'] = original_database_url
            else:
                os.environ.pop('DATABASE_URL', None)
        
        if total_articles == 0:
            self.stdout.write(self.style.WARNING('No published articles found.'))
            return
        
        # Collect article metadata
        article_data = []
        for article in articles:
            article_data.append({
                'title': article.title,
                'slug': article.slug,
                'language': article.language,
                'category': article.category,
                'topic_section': article.topic_section,
                'content': article.content,
            })
        
        # Identify missing semantic connections
        self.stdout.write(self.style.SUCCESS('=== SEMANTIC CONNECTION RECOMMENDATIONS ==='))
        self.stdout.write('')
        
        recommendations = self.generate_recommendations(article_data)
        
        if not recommendations:
            self.stdout.write(self.style.WARNING('No recommendations generated.'))
            return
        
        # Output recommendations
        for i, rec in enumerate(recommendations, 1):
            self.stdout.write(self.style.WARNING(f'--- Recommendation {i} ---'))
            self.stdout.write(f'Source Article: {rec["source_title"]} ({rec["source_slug"]})')
            self.stdout.write(f'Target Article: {rec["target_title"]} ({rec["target_slug"]})')
            self.stdout.write(f'Recommended Anchor: {rec["anchor_phrase"]}')
            self.stdout.write(f'Sentence to Add: {rec["sentence_to_add"]}')
            self.stdout.write(f'Relevance: {rec["relevance"]}')
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS(f'Total recommendations: {len(recommendations)}'))
    
    def generate_recommendations(self, article_data):
        """Generate recommendations for missing semantic connections."""
        recommendations = []
        
        # Define semantic relationships based on topic clusters
        semantic_relationships = [
            {
                'source_topics': ['dark'],
                'target_topics': ['stoic', 'transform', 'aimind'],
                'anchor_phrases': ['stoic philosophy', 'stoic principles', 'stoic mindset'],
                'sentence_templates': [
                    'This concept aligns with {anchor}, which teaches emotional resilience.',
                    'Understanding {anchor} can help navigate these psychological patterns.',
                    'The {anchor} approach offers practical tools for dealing with such situations.',
                ]
            },
            {
                'source_topics': ['breakup'],
                'target_topics': ['women', 'human', 'transform'],
                'anchor_phrases': ['emotional dependency', 'attachment theory', 'self-worth'],
                'sentence_templates': [
                    'Understanding {anchor} is crucial for healing after relationship loss.',
                    'Many people struggle with {anchor} during difficult transitions.',
                    'Breaking free from {anchor} patterns is essential for personal growth.',
                ]
            },
            {
                'source_topics': ['dopamine'],
                'target_topics': ['human', 'transform', 'aimind'],
                'anchor_phrases': ['reward system', 'motivation psychology', 'behavior patterns'],
                'sentence_templates': [
                    'The brain\'s {anchor} plays a key role in habit formation.',
                    'Understanding {anchor} helps explain why certain behaviors persist.',
                    'Optimizing {anchor} can lead to sustainable lifestyle changes.',
                ]
            },
            {
                'source_topics': ['human'],
                'target_topics': ['dopamine', 'women', 'transform'],
                'anchor_phrases': ['human behavior', 'psychological needs', 'emotional validation'],
                'sentence_templates': [
                    'Research in {anchor} reveals patterns in how we respond to stimuli.',
                    'Understanding {anchor} is fundamental to personal development.',
                    'The study of {anchor} provides insights into relationship dynamics.',
                ]
            },
            {
                'source_topics': ['stoic'],
                'target_topics': ['dark', 'transform', 'aimind'],
                'anchor_phrases': ['emotional control', 'mental resilience', 'philosophical approach'],
                'sentence_templates': [
                    'Practicing {anchor} can transform how we handle challenges.',
                    'The {anchor} philosophy emphasizes focusing on what we can control.',
                    'Developing {anchor} is a lifelong journey of self-improvement.',
                ]
            },
            {
                'source_topics': ['transform'],
                'target_topics': ['stoic', 'dopamine', 'aimind'],
                'anchor_phrases': ['self-transformation', 'personal growth', 'behavioral change'],
                'sentence_templates': [
                    'True {anchor} requires consistent effort and self-awareness.',
                    'The journey of {anchor} involves both internal and external changes.',
                    'Sustainable {anchor} happens gradually through small daily habits.',
                ]
            },
            {
                'source_topics': ['aimind'],
                'target_topics': ['human', 'transform', 'dopamine'],
                'anchor_phrases': ['artificial intelligence', 'human cognition', 'AI and psychology'],
                'sentence_templates': [
                    'The intersection of {anchor} and psychology offers fascinating insights.',
                    'Understanding {anchor} helps us appreciate both human and machine intelligence.',
                    'The field of {anchor} is reshaping how we think about consciousness.',
                ]
            },
            {
                'source_topics': ['women'],
                'target_topics': ['breakup', 'human', 'transform'],
                'anchor_phrases': ['emotional needs', 'relationship dynamics', 'self-identity'],
                'sentence_templates': [
                    'Understanding {anchor} is essential for healthy relationships.',
                    'Many women navigate complex {anchor} during major life transitions.',
                    'Exploring {anchor} can lead to greater self-understanding and empowerment.',
                ]
            },
        ]
        
        # Generate recommendations for each article
        for source_article in article_data:
            source_topic = source_article['category'] if source_article['language'] == 'HI' else source_article['topic_section']
            
            for relationship in semantic_relationships:
                if source_topic in relationship['source_topics']:
                    # Find matching target articles
                    for target_article in article_data:
                        if source_article['slug'] == target_article['slug']:
                            continue
                        
                        target_topic = target_article['category'] if target_article['language'] == 'HI' else target_article['topic_section']
                        
                        if target_topic in relationship['target_topics']:
                            # Check if anchor phrase already exists in source content
                            content_lower = source_article['content'].lower()
                            
                            for anchor_phrase in relationship['anchor_phrases']:
                                if anchor_phrase.lower() not in content_lower:
                                    # Generate recommendation
                                    sentence_template = relationship['sentence_templates'][0]
                                    sentence_to_add = sentence_template.format(anchor=anchor_phrase)
                                    
                                    recommendations.append({
                                        'source_title': source_article['title'],
                                        'source_slug': source_article['slug'],
                                        'target_title': target_article['title'],
                                        'target_slug': target_article['slug'],
                                        'anchor_phrase': anchor_phrase,
                                        'sentence_to_add': sentence_to_add,
                                        'relevance': f'Connects {source_topic} topic to {target_topic} topic through semantic relationship.',
                                    })
                                    
                                    # Only add one recommendation per source-target pair
                                    break
        
        return recommendations
