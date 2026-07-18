"""
Django management command: fix_onrender_links

WHAT THIS FIXES
----------------
15 of your 32 articles have internal links hardcoded to your Render
testing domain instead of your real domain, e.g.:

    https://storic-whisper.onrender.com/en/
    https://storic-whisper.onrender.com/articles/stoicism/

instead of:

    https://storicwhisper.com/en/
    https://storicwhisper.com/articles/stoicism/

This sends readers (and link authority) OFF your real domain, looks
unprofessional to anyone who clicks "Read next" inside an article, and
can create duplicate-content confusion between the two domains. This
command rewrites every such link in Article.content to point at
storicwhisper.com instead, keeping the path/query exactly as it was.

Worst offenders found:
    id=5  (stoicism)             -> 13 onrender.com links
    id=9  (self-transformation)  -> 16 onrender.com links
    id=7  (Human-Behavior)       -> 14 onrender.com links
    + 12 more articles with 1-3 links each

SAFETY
------
- Only touches the hostname. Path, query string, anchor text, and
  everything else in the link stays identical.
- Nothing is deleted. Every changed article's ORIGINAL content is saved
  to ArticleContentBackup before the Article row is updated, tagged
  with a run_id so you can find/restore it later.
- Run with --dry-run first to preview every replacement before writing
  anything.

USAGE
-----
    # 1. Preview only, touches nothing:
    python manage.py fix_onrender_links --dry-run

    # 2. Test on a single article first:
    python manage.py fix_onrender_links --slug stoicism --dry-run
    python manage.py fix_onrender_links --slug stoicism --apply

    # 3. Once happy, run for everything:
    python manage.py fix_onrender_links --apply

    # 4. To find the backups from this run afterwards:
    python manage.py shell
    >>> from core.models import ArticleContentBackup
    >>> ArticleContentBackup.objects.filter(run_id="fix_onrender_links_20260718_...")

INSTALL LOCATION
----------------
Copy this file next to fix_broken_article_html.py:
    core/management/commands/fix_onrender_links.py
"""

import re
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Article, ArticleContentBackup


# Matches http(s)://<anything>.onrender.com  (any subdomain, http or https)
ONRENDER_PATTERN = re.compile(
    r'https?://[a-zA-Z0-9\-]+\.onrender\.com',
    re.IGNORECASE,
)

REAL_DOMAIN = 'https://storicwhisper.com'


def fix_onrender_links(text: str):
    """
    Replace every http(s)://<sub>.onrender.com occurrence with
    https://storicwhisper.com, keeping the rest of the URL untouched.
    Returns (new_text, num_links_replaced, matched_urls_sample).
    """
    matches = ONRENDER_PATTERN.findall(text)
    if not matches:
        return text, 0, []

    new_text = ONRENDER_PATTERN.sub(REAL_DOMAIN, text)
    sample = sorted(set(matches))
    return new_text, len(matches), sample


class Command(BaseCommand):
    help = "Rewrite internal links pointing at *.onrender.com to storicwhisper.com in Article.content."

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true',
                             help='Actually write changes to the database. Without this flag, nothing is saved.')
        parser.add_argument('--dry-run', action='store_true',
                             help='Preview changes only (default behavior if --apply is not passed).')
        parser.add_argument('--slug', type=str, default=None,
                             help='Only process a single article by slug (useful for testing first).')

    def handle(self, *args, **options):
        apply_changes = options['apply']
        target_slug = options['slug']

        qs = Article.objects.all().order_by('id')
        if target_slug:
            qs = qs.filter(slug=target_slug)
            if not qs.exists():
                self.stdout.write(self.style.ERROR(f"No article found with slug='{target_slug}'"))
                return

        run_id = "fix_onrender_links_" + datetime.now().strftime("%Y%m%d_%H%M%S")

        total_articles_scanned = 0
        articles_changed = 0
        total_links_fixed = 0

        self.stdout.write(self.style.WARNING(
            f"\nMode: {'APPLY (writing to DB)' if apply_changes else 'DRY RUN (no changes will be saved)'}\n"
        ))

        for article in qs:
            total_articles_scanned += 1
            original = article.content

            cleaned, num_fixed, sample_urls = fix_onrender_links(original)

            if num_fixed == 0:
                continue

            articles_changed += 1
            total_links_fixed += num_fixed

            self.stdout.write(self.style.HTTP_INFO(
                f"\n[id={article.id}] [{article.language}] {article.slug}"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"  {num_fixed} onrender.com link(s) -> storicwhisper.com  (e.g. {sample_urls[0]})"
            ))

            if apply_changes:
                with transaction.atomic():
                    ArticleContentBackup.objects.create(
                        article=article,
                        content_before=original,
                        run_id=run_id,
                    )
                    article.content = cleaned
                    article.save(update_fields=['content', 'updated_at'])
                self.stdout.write(self.style.SUCCESS("  -> saved, original backed up to ArticleContentBackup"))

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(f"Scanned:            {total_articles_scanned} article(s)")
        self.stdout.write(f"Articles changed:   {articles_changed}")
        self.stdout.write(f"Total links fixed:  {total_links_fixed}")
        if apply_changes:
            self.stdout.write(self.style.SUCCESS(f"\nChanges saved. Backup run_id = {run_id}"))
        else:
            self.stdout.write(self.style.WARNING(
                "\nThis was a DRY RUN — nothing was saved. Re-run with --apply to write these changes."
            ))
            