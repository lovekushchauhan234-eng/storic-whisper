from django.core.management.base import BaseCommand
from core.models import Article
from core.views import ENGLISH_HUB_TOPICS


class Command(BaseCommand):
    help = 'Diagnose latest_articles queryset issue'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== DIAGNOSING LATEST ARTICLES ==='))
        
        # 1. Total English articles
        base_qs = Article.objects.filter(
            is_published=True,
            language='EN',
        ).order_by('-created_at')
        
        total_en = base_qs.count()
        self.stdout.write(f'\n1. Total English articles (is_published=True, language=EN): {total_en}')
        
        # 2. latest_articles queryset
        latest_articles = list(base_qs[:3])
        self.stdout.write(f'\n2. latest_articles length: {len(latest_articles)}')
        
        if latest_articles:
            self.stdout.write('\n   Latest articles:')
            for i, article in enumerate(latest_articles, 1):
                self.stdout.write(f'   {i}. ID={article.id} | Title="{article.title}" | Language={article.language} | Topic={article.topic_section} | Published={article.is_published}')
        else:
            self.stdout.write('   No articles found')
        
        # 3. SQL query for latest_articles
        self.stdout.write(f'\n3. SQL query for latest_articles:')
        self.stdout.write(f'   {str(base_qs[:3].query)}')
        
        # 4. Distinct language values in database
        all_languages = Article.objects.values_list('language', flat=True).distinct()
        self.stdout.write(f'\n4. Distinct language values in database: {list(all_languages)}')
        
        # 5. Total articles by language
        for lang in all_languages:
            count = Article.objects.filter(language=lang).count()
            published_count = Article.objects.filter(language=lang, is_published=True).count()
            self.stdout.write(f'   Language={lang}: Total={count}, Published={published_count}')
        
        # 6. topic_sections queryset comparison
        self.stdout.write(f'\n5. topic_sections queryset analysis:')
        topic_sections = []
        for key, label in ENGLISH_HUB_TOPICS:
            section_articles = list(base_qs.filter(topic_section=key))
            if section_articles:
                self.stdout.write(f'   Topic="{key}" ({label}): {len(section_articles)} articles')
                for i, article in enumerate(section_articles[:3], 1):
                    self.stdout.write(f'      {i}. ID={article.id} | Title="{article.title}" | Language={article.language} | Topic={article.topic_section}')
            else:
                self.stdout.write(f'   Topic="{key}" ({label}): 0 articles')
        
        # 6. Check if topic_sections has any articles
        total_in_sections = sum(len(list(base_qs.filter(topic_section=key))) for key, _ in ENGLISH_HUB_TOPICS)
        self.stdout.write(f'\n6. Total articles across all topic_sections: {total_in_sections}')
        
        # 7. Root cause analysis
        self.stdout.write(f'\n=== ROOT CAUSE ANALYSIS ===')
        if total_en == 0:
            self.stdout.write('   RESULT: No English articles exist in database')
            self.stdout.write('   EXPLANATION: latest_articles is empty because there are no English articles')
        elif len(latest_articles) == 0 and total_en > 0:
            self.stdout.write('   RESULT: English articles exist but latest_articles is empty')
            self.stdout.write('   EXPLANATION: Queryset evaluation issue or filter problem')
        elif len(latest_articles) > 0:
            self.stdout.write('   RESULT: latest_articles has articles')
            self.stdout.write('   EXPLANATION: Code is working correctly')
        
        if total_in_sections > 0 and len(latest_articles) == 0:
            self.stdout.write('   CRITICAL: topic_sections has articles but latest_articles is empty')
            self.stdout.write('   This indicates a queryset evaluation order issue')
