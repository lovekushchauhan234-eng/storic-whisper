"""
Django management command: fix_broken_article_html

WHAT THIS FIXES
----------------
1. CRITICAL BUG: ~18 of your 32 live articles have a FULL standalone HTML
   document (<!DOCTYPE html><html><head><style>...</style></head><body>...)
   saved inside Article.content. Because article_detail.html already
   extends base.html (which prints its own <!DOCTYPE>/<html>/<head>/<body>),
   this produces INVALID, NESTED double-HTML on the live page.
   This script strips the outer wrapper and keeps only the real article
   body (the <article>...</article> or <main>...</main> block).

2. STRAY CJK / GARBLED CHARACTERS: a handful of articles have random
   Chinese characters glued mid-word into Hindi text (an unreviewed
   AI/translation pipeline leak, e.g. "डोपामिन लेवल变स्पाइक"). This
   script strips CJK Unicode ranges from ALL article content, since your
   site never intentionally uses Chinese script.

SAFETY
------
- Nothing is deleted. Every changed article's ORIGINAL content is saved
  to ArticleContentBackup (the model you already have) before the
  Article row is updated, tagged with a run_id so you can find/restore it.
- Run with --dry-run first. It prints exactly what would change for each
  article (diff-style preview) WITHOUT touching the database.
- Then run for real with --apply.
- You can also target a single article with --slug <slug> to test on one
  article first.

USAGE
-----
    # 1. See what would change, touch nothing:
    python manage.py fix_broken_article_html --dry-run

    # 2. Try it on exactly one article first:
    python manage.py fix_broken_article_html --slug how-ai-is-rewiring-the-human-mind-the-hidden-psych --dry-run
    python manage.py fix_broken_article_html --slug how-ai-is-rewiring-the-human-mind-the-hidden-psych --apply

    # 3. Once happy, run for everything:
    python manage.py fix_broken_article_html --apply

    # 4. If something looks wrong afterwards, every backup is sitting in
    #    ArticleContentBackup, filtered by the run_id printed at the end:
    python manage.py shell
    >>> from core.models import ArticleContentBackup
    >>> ArticleContentBackup.objects.filter(run_id="fix_html_20260718_153000")

INSTALL LOCATION
----------------
Copy this file to:
    core/management/commands/fix_broken_article_html.py

(Django needs the core/management/ and core/management/commands/ folders
to each contain an __init__.py file. If you don't already have them from
your other management commands, create empty __init__.py files there too.)
"""

import re
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Article, ArticleContentBackup

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # we check for this in handle()


# Chinese/CJK Unicode ranges that should NEVER legitimately appear in this
# site's Hindi/English content. Anything in these ranges is a generation
# glitch, not real content.
CJK_PATTERN = re.compile(
    r'[\u4e00-\u9fff'      # CJK Unified Ideographs
    r'\u3400-\u4dbf'       # CJK Extension A
    r'\u3040-\u30ff'       # Hiragana / Katakana
    r'\uac00-\ud7af'       # Hangul syllables
    r']+'
)


def strip_cjk(text: str) -> tuple[str, int]:
    """Remove stray CJK characters. Returns (clean_text, num_removed_chars)."""
    matches = CJK_PATTERN.findall(text)
    removed = sum(len(m) for m in matches)
    if removed:
        text = CJK_PATTERN.sub('', text)
    return text, removed


def unwrap_full_html_document(raw_content: str):
    """
    If raw_content is a full standalone HTML document (has <!DOCTYPE html>
    or an <html> root), extract just the real article body and drop the
    duplicate <!DOCTYPE>/<html>/<head>/<style>/<body> wrapper.

    Returns (new_content, was_broken: bool, note: str)
    """
    stripped = raw_content.lstrip()
    looks_like_full_doc = (
        stripped[:15].lower().startswith('<!doctype html')
        or stripped[:6].lower().startswith('<html')
        or ('<head>' in raw_content[:400].lower() and '<style' in raw_content[:2000].lower())
    )

    if not looks_like_full_doc:
        return raw_content, False, "already clean, left untouched"

    if BeautifulSoup is None:
        return raw_content, True, "SKIPPED — beautifulsoup4 not installed, run: pip install beautifulsoup4"

    soup = BeautifulSoup(raw_content, 'html.parser')

    # Preference order: <article> tag > <main> tag > everything inside <body>
    inner = soup.find('article')
    source = 'article'
    if inner is None:
        inner = soup.find('main')
        source = 'main'
    if inner is None:
        inner = soup.find('body')
        source = 'body'

    if inner is None:
        # Nothing recognizable — bail out safely rather than guess wrong.
        return raw_content, True, "SKIPPED — could not find <article>/<main>/<body>, needs manual review"

    new_content = inner.decode_contents().strip()
    note = f"unwrapped duplicate <!DOCTYPE>/<html>/<head>/<style>/<body>, kept inner <{source}> content"
    return new_content, True, note


class Command(BaseCommand):
    help = "Fix articles whose content field contains a full nested HTML document, and strip stray CJK glitch characters."

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

        if BeautifulSoup is None:
            self.stdout.write(self.style.ERROR(
                "beautifulsoup4 is not installed in this environment. "
                "It IS already in your requirements.txt (beautifulsoup4==4.14.3), "
                "so on Render it should be present. Locally run: pip install beautifulsoup4"
            ))
            return

        qs = Article.objects.all().order_by('id')
        if target_slug:
            qs = qs.filter(slug=target_slug)
            if not qs.exists():
                self.stdout.write(self.style.ERROR(f"No article found with slug='{target_slug}'"))
                return

        run_id = "fix_html_" + datetime.now().strftime("%Y%m%d_%H%M%S")

        total = 0
        html_fixed = 0
        cjk_fixed = 0
        skipped = []

        self.stdout.write(self.style.WARNING(
            f"\nMode: {'APPLY (writing to DB)' if apply_changes else 'DRY RUN (no changes will be saved)'}\n"
        ))

        for article in qs:
            total += 1
            original = article.content

            unwrapped, was_broken, note = unwrap_full_html_document(original)
            cleaned, cjk_removed = strip_cjk(unwrapped)

            changed = cleaned != original

            if not changed:
                continue

            self.stdout.write(self.style.HTTP_INFO(
                f"\n[id={article.id}] [{article.language}] {article.slug}"
            ))
            if was_broken:
                if "SKIPPED" in note:
                    self.stdout.write(self.style.ERROR(f"  HTML wrapper: {note}"))
                    skipped.append(article.slug)
                else:
                    self.stdout.write(self.style.SUCCESS(f"  HTML wrapper: {note}"))
                    self.stdout.write(f"    before: {len(original):,} chars  ->  after: {len(cleaned):,} chars")
                    html_fixed += 1
            if cjk_removed:
                self.stdout.write(self.style.SUCCESS(f"  Removed {cjk_removed} stray CJK character(s)"))
                cjk_fixed += 1

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
        self.stdout.write(f"Scanned:            {total} article(s)")
        self.stdout.write(f"HTML wrapper fixed: {html_fixed}")
        self.stdout.write(f"CJK glitches fixed: {cjk_fixed}")
        if skipped:
            self.stdout.write(self.style.WARNING(
                f"Needs manual review (couldn't safely auto-extract): {', '.join(skipped)}"
            ))
        if apply_changes:
            self.stdout.write(self.style.SUCCESS(f"\nChanges saved. Backup run_id = {run_id}"))
        else:
            self.stdout.write(self.style.WARNING(
                "\nThis was a DRY RUN — nothing was saved. Re-run with --apply to write these changes."
            ))
            