import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Article
from .pillar_helpers import get_related_articles
from .luppi import chat as luppi_chat


ENGLISH_HUB_TOPICS = [
    ('attachment', 'Attachment Theory & Traumas'),
    ('validation', 'Validation Psychology'),
    ('dependency', 'Emotional Dependency'),
    ('relationship', 'Relationship Dynamics'),
    ('dark', 'Dark Psychology Awareness'),
    ('stoicism', 'Practical Stoicism'),
    ('dopamine', 'Dopamine & Modern Mind'),
    ('transformation', 'Self Transformation'),
    ('behavior', 'Human Behavior Insights'),
    ('ai_mind', 'AI & The Human Mind'),
]


# ---------- BASIC PAGES ----------

def home(request):
    hindi_qs = Article.objects.filter(is_published=True, language='HI')
    featured_articles = hindi_qs.order_by('-created_at')[:3]
    english_posts = (
        Article.objects.filter(is_published=True, language='EN')
        .order_by('-created_at')[:6]
    )
    # BUG 1 FIX: Add most_read_articles and cornerstone_articles
    most_read_articles = hindi_qs.order_by('-created_at')[:3]
    cornerstone_articles = hindi_qs.filter(is_featured=True)[:3]
    return render(request, 'core/home.html', {
        'featured_articles': featured_articles,
        'english_posts': english_posts,
        'most_read_articles': most_read_articles,
        'cornerstone_articles': cornerstone_articles,
    })


def english_hub(request):
    topic_labels = dict(ENGLISH_HUB_TOPICS)

    articles = list(
        Article.objects.filter(is_published=True, language='EN')
        .order_by('-created_at')
    )
    for a in articles:
        a.topic_label = topic_labels.get(a.topic_section, 'Psychology')

    # Only topics that actually have at least one live article get a filter chip —
    # this guarantees the hub never shows an empty/"coming soon" section.
    topic_counts = {}
    for a in articles:
        topic_counts[a.topic_section] = topic_counts.get(a.topic_section, 0) + 1

    topics = [
        {'key': key, 'label': label, 'count': topic_counts[key]}
        for key, label in ENGLISH_HUB_TOPICS
        if topic_counts.get(key)
    ]

    return render(request, 'core/english_hub.html', {
        'articles': articles,
        'topics': topics,
        'total_articles': len(articles),
        'topic_count': len(topics),
    })


def women(request):
    return render(request, 'core/women.html', {
        'related_articles': get_related_articles('women'),
    })


def stoicism(request):
    return render(request, 'core/stoicism.html', {
        'related_articles': get_related_articles('stoic'),
    })


def breakup(request):
    return render(request, 'core/breakup.html', {
        'related_articles': get_related_articles('breakup'),
    })


def about(request):
    return render(request, 'core/about.html')


def dark_psychology(request):
    return render(request, 'core/dark.html', {
        'related_articles': get_related_articles('dark'),
    })


def dopamine(request):
    return render(request, 'core/dopamine.html', {
        'related_articles': get_related_articles('dopamine'),
    })


def human_behavior(request):
    return render(request, 'core/human_behavior.html', {
        'related_articles': get_related_articles('human'),
    })


def self_transform(request):
    return render(request, 'core/self_transform.html', {
        'related_articles': get_related_articles('transform'),
    })


def ai_mind(request):
    return render(request, 'core/ai_mind.html', {
        'related_articles': get_related_articles('aimind'),
    })


def privacy(request):
    return render(request, 'core/privacy.html')


def terms(request):
    return render(request, 'core/terms.html')


def disclaimer(request):
    return render(request, 'core/disclaimer.html')


def contact(request):
    return render(request, 'core/contact.html')


# ---------- AI SAATHI ----------

def ai_assistant(request):
    return render(request, 'core/ai_assistant.html')


@require_POST
def luppi_chat_api(request):
    """LUPPI intelligence API — session memory, domain routing, structured replies."""
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    message = (payload.get('message') or '').strip()
    if not message:
        return JsonResponse({'error': 'Message required'}, status=400)
    if len(message) > 4000:
        return JsonResponse({'error': 'Message too long'}, status=400)

    response = luppi_chat(request, message)
    return JsonResponse(response.to_dict())


# ---------- NEWSLETTER ----------

def subscribe(request):
    """Save newsletter subscriber email."""
    if request.method == 'POST':
        from .models import Subscriber
        email = request.POST.get('email', '').strip()
        if email and '@' in email and '.' in email:
            Subscriber.objects.get_or_create(email=email)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ---------- ARTICLES ----------

def article_list(request):
    articles = (
        Article.objects.filter(is_published=True, language='HI')
        .order_by('-created_at')
    )

    return render(request, 'core/article_list.html', {
        'articles': articles
    })


def get_article_related_articles(article, limit=3):
    """Get related articles based on language and category/topic_section."""
    if article.language == 'EN':
        # English: Use topic_section first, fallback to category
        if article.topic_section:
            related = Article.objects.filter(
                is_published=True,
                language='EN',
                topic_section=article.topic_section
            ).exclude(slug=article.slug).order_by('-created_at')[:limit]
            if len(related) >= limit:
                return list(related)
        # Fallback to category
        related = Article.objects.filter(
            is_published=True,
            language='EN',
            category=article.category
        ).exclude(slug=article.slug).order_by('-created_at')[:limit]
        return list(related)
    else:
        # Hindi: Use category
        related = Article.objects.filter(
            is_published=True,
            language='HI',
            category=article.category
        ).exclude(slug=article.slug).order_by('-created_at')[:limit]
        return list(related)


def get_previous_next_articles(article):
    """Get previous and next articles based on language, category, and created_at."""
    # Try same language + category first
    previous = Article.objects.filter(
        is_published=True,
        language=article.language,
        category=article.category,
        created_at__lt=article.created_at
    ).order_by('-created_at').first()
    
    next = Article.objects.filter(
        is_published=True,
        language=article.language,
        category=article.category,
        created_at__gt=article.created_at
    ).order_by('created_at').first()
    
    # Fallback to same language only if no results
    if not previous and not next:
        previous = Article.objects.filter(
            is_published=True,
            language=article.language,
            created_at__lt=article.created_at
        ).order_by('-created_at').first()
        
        next = Article.objects.filter(
            is_published=True,
            language=article.language,
            created_at__gt=article.created_at
        ).order_by('created_at').first()
    
    return previous, next


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    
    related_articles = get_article_related_articles(article, limit=3)
    previous_article, next_article = get_previous_next_articles(article)

    return render(request, 'core/article_detail.html', {
        'article': article,
        'related_articles': related_articles,
        'previous_article': previous_article,
        'next_article': next_article,
    })
    