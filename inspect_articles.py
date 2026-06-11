import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storic_whisper_site.settings')
django.setup()

from core.models import Article

print("=" * 60)
print("ARTICLE DATA INSPECTION")
print("=" * 60)

print("\n1. TOTAL ARTICLES:")
print(Article.objects.count())

print("\n2. DISTINCT LANGUAGES:")
languages = Article.objects.values_list('language', flat=True).distinct()
for lang in languages:
    print(f"  '{lang}'")

print("\n3. PUBLISHED EN (uppercase):")
print(Article.objects.filter(is_published=True, language='EN').count())

print("\n4. PUBLISHED en (lowercase):")
print(Article.objects.filter(is_published=True, language='en').count())

print("\n5. DISTINCT topic_section VALUES:")
topic_sections = Article.objects.values_list('topic_section', flat=True).distinct()
for topic in topic_sections:
    print(f"  '{topic}'")

print("\n6. FIRST 20 ARTICLES (ID, title, language, is_published, topic_section):")
articles = Article.objects.all()[:20]
for article in articles:
    print(f"  ID: {article.id}")
    print(f"    Title: {article.title}")
    print(f"    Language: '{article.language}'")
    print(f"    Published: {article.is_published}")
    print(f"    Topic: '{article.topic_section}'")
    print()

print("\n7. PUBLISHED ARTICLES BY LANGUAGE:")
for lang in languages:
    count = Article.objects.filter(is_published=True, language=lang).count()
    print(f"  Language '{lang}': {count} published")

print("\n8. ENGLISH ARTICLES (case-insensitive):")
english_count = Article.objects.filter(is_published=True, language__iexact='EN').count()
print(f"  Total: {english_count}")

print("\n" + "=" * 60)
