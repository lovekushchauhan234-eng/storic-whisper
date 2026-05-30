from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article


# ── 1. Static Pages ────────────────────────────────────────────
class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority    = 0.8
    protocol    = 'https'

    def items(self):
        return [
            'home',
            'breakup',
            'women',
            'dark',
            'stoicism',
            'dopamine',
            'human_behavior',
            'self_transform',
            'ai_mind',
            'about',
            'article_list',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            'home':           1.0,
            'breakup':        0.9,
            'women':          0.9,
            'dark':           0.9,
            'stoicism':       0.9,
            'dopamine':       0.8,
            'human_behavior': 0.8,
            'self_transform': 0.8,
            'ai_mind':        0.8,
            'article_list':   0.8,
            'about':          0.6,
        }
        return priorities.get(item, 0.7)


# ── 2. Article Pages ───────────────────────────────────────────
class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority    = 0.9
    protocol    = 'https'

    def items(self):
        return Article.objects.filter(is_published=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('article_detail', args=[obj.slug])