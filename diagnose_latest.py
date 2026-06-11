import os
import sys
import django

# Accept database URL as command line argument
if len(sys.argv) > 1:
    database_url = sys.argv[1]
    os.environ['DATABASE_URL'] = database_url
    print(f'Using DATABASE_URL from command line argument')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storic_whisper_site.settings')
django.setup()

from django.conf import settings
from core.models import Article
from core.views import ENGLISH_HUB_TOPICS

print(f'Database engine: {settings.DATABASES["default"]["ENGINE"]}')
print(f'Database name: {settings.DATABASES["default"]["NAME"]}')
print()

print('=== DIAGNOSTICS ===\n')

# 1. Total English articles
base_qs = Article.objects.filter(
    is_published=True,
    language='EN',
).order_by('-created_at')

total_en = base_qs.count()
print(f'1. Total English articles (is_published=True, language=EN): {total_en}')

# 2. latest_articles queryset
latest_articles = list(base_qs[:3])
print(f'\n2. latest_articles length: {len(latest_articles)}')

if latest_articles:
    print('   Latest articles:')
    for i, article in enumerate(latest_articles, 1):
        print(f'   {i}. ID={article.id} | Title="{article.title}" | Language={article.language} | Topic={article.topic_section} | Published={article.is_published}')
else:
    print('   No articles found')

# 3. SQL query for latest_articles
print(f'\n3. SQL query for latest_articles:')
print(f'   {str(base_qs[:3].query)}')

# 4. Distinct language values in database
all_languages = Article.objects.values_list('language', flat=True).distinct()
print(f'\n4. Distinct language values in database: {list(all_languages)}')

# 5. Total articles by language
for lang in all_languages:
    count = Article.objects.filter(language=lang).count()
    published_count = Article.objects.filter(language=lang, is_published=True).count()
    print(f'   Language={lang}: Total={count}, Published={published_count}')

# 6. topic_sections queryset comparison
print(f'\n5. topic_sections queryset analysis:')
total_in_sections = 0
for key, label in ENGLISH_HUB_TOPICS:
    section_articles = list(base_qs.filter(topic_section=key))
    if section_articles:
        print(f'   Topic="{key}" ({label}): {len(section_articles)} articles')
        for i, article in enumerate(section_articles[:3], 1):
            print(f'      {i}. ID={article.id} | Title="{article.title}" | Language={article.language} | Topic={article.topic_section}')
        total_in_sections += len(section_articles)
    else:
        print(f'   Topic="{key}" ({label}): 0 articles')

print(f'\n6. Total articles across all topic_sections: {total_in_sections}')

# 7. Root cause analysis
print(f'\n=== ROOT CAUSE ANALYSIS ===')
if total_en == 0:
    print('   RESULT: No English articles exist in database')
    print('   EXPLANATION: latest_articles is empty because there are no English articles')
elif len(latest_articles) == 0 and total_en > 0:
    print('   RESULT: English articles exist but latest_articles is empty')
    print('   EXPLANATION: Queryset evaluation issue or filter problem')
elif len(latest_articles) > 0:
    print('   RESULT: latest_articles has articles')
    print('   EXPLANATION: Code is working correctly')

if total_in_sections > 0 and len(latest_articles) == 0:
    print('   CRITICAL: topic_sections has articles but latest_articles is empty')
    print('   This indicates a queryset evaluation order issue')
