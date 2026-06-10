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
    
    # Cornerstone content for "Start Here" section - get most recent from each category
    cornerstone_articles = []
    categories = ['breakup', 'women', 'dark', 'stoic', 'dopamine', 'human', 'transform', 'aimind']
    for cat in categories:
        article = Article.objects.filter(
            is_published=True,
            category=cat,
            language='HI'
        ).order_by('-created_at').first()
        if article:
            cornerstone_articles.append(article)
    
    return render(request, 'core/home.html', {
        'featured_articles': featured_articles,
        'english_posts': english_posts,
        'cornerstone_articles': cornerstone_articles,
    })


def english_hub(request):
    base_qs = Article.objects.filter(
        is_published=True,
        language='EN',
    ).order_by('-created_at')

    topic_sections = []
    for key, label in ENGLISH_HUB_TOPICS:
        topic_sections.append({
            'key': key,
            'label': label,
            'articles': list(base_qs.filter(topic_section=key)),
        })

    latest_articles = base_qs[:3]
    total_articles = base_qs.count()

    return render(request, 'core/english_hub.html', {
        'topic_sections': topic_sections,
        'latest_articles': latest_articles,
        'total_articles': total_articles,
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


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)

    return render(request, 'core/article_detail.html', {
        'article': article
    })