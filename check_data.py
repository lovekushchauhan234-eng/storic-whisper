import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storic_whisper_site.settings')
django.setup()

from core.models import Article

print('Total articles:', Article.objects.count())
print('\nBy language:')
print('  HI:', Article.objects.filter(language='HI').count())
print('  EN:', Article.objects.filter(language='EN').count())

print('\nCategory usage:')
for cat, label in Article.CATEGORY_CHOICES:
    count = Article.objects.filter(category=cat).count()
    if count > 0:
        print(f'  {cat} ({label}): {count}')

print('\nTopic section usage:')
for topic, label in Article.TOPIC_SECTION_CHOICES:
    count = Article.objects.filter(topic_section=topic).count()
    if count > 0:
        print(f'  {topic} ({label}): {count}')

print('\nSample data:')
for article in Article.objects.all()[:5]:
    print(f'  {article.title[:40]}... | lang={article.language} | cat={article.category} | topic={article.topic_section}')
