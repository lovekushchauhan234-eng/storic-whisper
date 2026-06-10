from core.models import Article, ArticleLink, ArticleContentBackup
from core.linking.scorer import calculate_link_score
from core.linking.injector import inject_link
from django.utils import timezone
from datetime import datetime
import uuid


def generate_run_id():
    """Generate a unique run ID for tracking link generation."""
    return f"links_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"


def get_link_candidates(source_article, min_score=0.5):
    """
    Get and score candidate articles for linking.
    Returns list of (target_article, score) tuples sorted by score descending.
    """
    candidates = []
    
    # Query eligible targets (same language, is_published=True, not self)
    targets = Article.objects.filter(
        is_published=True,
        language=source_article.language
    ).exclude(id=source_article.id)
    
    for target in targets:
        score = calculate_link_score(source_article, target)
        if score >= min_score:
            candidates.append((target, score))
    
    # Sort by score descending
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates


def generate_anchor_candidates(target_article):
    """
    Generate anchor text candidates for a target article.
    Fallback hierarchy: keyword → topic → category → title fragments
    Returns list of anchor candidates in priority order.
    """
    candidates = []
    
    # 1. Keywords (if available)
    # Note: This would require a keywords field on the Article model
    # For now, skip as the model doesn't have this field
    
    # 2. Topic section (English) or Category (Hindi)
    if target_article.language == 'EN' and target_article.topic_section:
        # Get topic display name
        topic_display = dict(Article.TOPIC_SECTION_CHOICES).get(target_article.topic_section)
        if topic_display:
            candidates.append(topic_display)
    elif target_article.language == 'HI' and target_article.category:
        # Get category display name
        category_display = dict(Article.CATEGORY_CHOICES).get(target_article.category)
        if category_display:
            candidates.append(category_display)
    
    # 3. Category (English) or Topic (Hindi) as fallback
    if target_article.language == 'EN' and target_article.category:
        category_display = dict(Article.CATEGORY_CHOICES).get(target_article.category)
        if category_display:
            candidates.append(category_display)
    elif target_article.language == 'HI' and target_article.topic_section:
        topic_display = dict(Article.TOPIC_SECTION_CHOICES).get(target_article.topic_section)
        if topic_display:
            candidates.append(topic_display)
    
    # 4. Title fragments (first 3-4 words)
    title_words = target_article.title.split()
    if len(title_words) >= 3:
        candidates.append(' '.join(title_words[:3]))
    if len(title_words) >= 4:
        candidates.append(' '.join(title_words[:4]))
    
    # 5. Full title as last resort
    candidates.append(target_article.title)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_candidates = []
    for candidate in candidates:
        if candidate and candidate.lower() not in seen:
            seen.add(candidate.lower())
            unique_candidates.append(candidate)
    
    return unique_candidates


def generate_links_for_article(article, max_links=3, min_score=0.5, dry_run=True, run_id=None):
    """
    Generate internal links for a single article.
    
    Args:
        article: The source Article object
        max_links: Maximum number of links to add
        min_score: Minimum score threshold for including a link
        dry_run: If True, only propose changes without writing
        run_id: Run ID for tracking (generated if not provided)
    
    Returns:
        Dictionary with results including proposed_links, skipped_links, etc.
    """
    if run_id is None:
        run_id = generate_run_id()
    
    results = {
        'article': article,
        'run_id': run_id,
        'proposed_links': [],
        'skipped_duplicates': [],
        'skipped_below_score': [],
        'skipped_injection_failed': [],
    }
    
    # Get and score candidates
    candidates = get_link_candidates(article, min_score)
    
    # Take top max_links
    candidates = candidates[:max_links]
    
    for target, score in candidates:
        # Check if link already exists
        existing = ArticleLink.objects.filter(
            source_article=article,
            target_article=target
        ).exists()
        
        if existing:
            results['skipped_duplicates'].append({
                'target': target,
                'score': score,
                'reason': 'Link already exists'
            })
            continue
        
        if not dry_run:
            # Create backup
            ArticleContentBackup.objects.create(
                article=article,
                content_before=article.content,
                run_id=run_id
            )
            
            # Generate anchor candidates using fallback hierarchy
            anchor_candidates = generate_anchor_candidates(target)
            
            # Inject link into content
            modified_content = inject_link(article.content, anchor_candidates, target)
            
            if modified_content == article.content:
                # Injection failed
                results['skipped_injection_failed'].append({
                    'target': target,
                    'score': score,
                    'reason': 'No anchor candidate found in content'
                })
                continue
            
            # Save modified content
            article.content = modified_content
            article.save()
            
            # Create ArticleLink record with the actual anchor used
            ArticleLink.objects.create(
                source_article=article,
                target_article=target,
                anchor_text=anchor_candidates[0],  # First successful candidate
                link_type='auto_category',
                is_active=True,
                created_by_run=run_id
            )
        
        results['proposed_links'].append({
            'target': target,
            'score': score,
            'anchor_candidates': generate_anchor_candidates(target)
        })
    
    return results


def rollback_run(run_id):
    """
    Rollback all changes from a specific run.
    
    Args:
        run_id: The run ID to rollback
    
    Returns:
        Dictionary with rollback results
    """
    results = {
        'run_id': run_id,
        'articles_restored': 0,
        'links_deactivated': 0,
        'errors': []
    }
    
    # Find all backups for this run
    backups = ArticleContentBackup.objects.filter(run_id=run_id)
    
    for backup in backups:
        try:
            # Restore content
            backup.article.content = backup.content_before
            backup.article.save()
            results['articles_restored'] += 1
        except Exception as e:
            results['errors'].append({
                'article': backup.article.slug,
                'error': str(e)
            })
    
    # Deactivate links from this run
    links = ArticleLink.objects.filter(created_by_run=run_id)
    for link in links:
        link.is_active = False
        link.save()
        results['links_deactivated'] += 1
    
    return results
