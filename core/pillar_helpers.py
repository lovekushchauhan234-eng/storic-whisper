from .models import Article


def get_related_articles(category=None, limit=3):
    """Published articles for pillar pages; backfill from other categories if needed."""
    base = Article.objects.filter(
        is_published=True,
        language='HI',
    ).order_by('-created_at')
    if not category:
        return list(base[:limit])

    matched = list(base.filter(category=category)[:limit])
    if len(matched) >= limit:
        return matched

    exclude_ids = [a.pk for a in matched]
    filler = base.exclude(pk__in=exclude_ids)[: limit - len(matched)]
    return matched + list(filler)
