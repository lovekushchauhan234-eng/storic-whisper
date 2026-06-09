from core.models import Article
from datetime import timedelta
from django.utils import timezone


def calculate_link_score(source_article, target_article):
    """
    Calculate link score for Phase 1 (13 articles).
    Score is a float 0.0-1.0. Links below min-score are excluded.
    
    Scoring signals:
    - Same category (HI) or topic_section (EN): +0.6
    - Same language: Required (hard-block)
    - Target is is_featured=True: +0.2
    - Target is recently published: +0.1
    - Target already has 5+ inbound links: -0.1
    - Link already exists (duplicate): SKIP
    """
    # Hard block: cross-language links
    if source_article.language != target_article.language:
        return 0.0
    
    # Hard block: self-links
    if source_article.id == target_article.id:
        return 0.0
    
    score = 0.0
    
    # Same category (Hindi) or topic_section (English)
    if source_article.language == 'HI':
        if source_article.category == target_article.category:
            score += 0.6
    else:  # English
        if source_article.topic_section == target_article.topic_section:
            score += 0.6
    
    # Target is featured
    if target_article.is_featured:
        score += 0.2
    
    # Recency bonus (published within 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    if target_article.created_at >= thirty_days_ago:
        score += 0.1
    
    # Inbound link concentration penalty
    inbound_count = target_article.inbound_links.filter(is_active=True).count()
    if inbound_count >= 5:
        score -= 0.1
    
    return min(max(score, 0.0), 1.0)  # Clamp between 0.0 and 1.0
