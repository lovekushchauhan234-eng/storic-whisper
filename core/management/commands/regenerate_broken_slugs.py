"""
Fixes the broken/ugly slugs flagged by `fix_adsense_trust_issues` (leading
hyphens, uppercase, mid-word truncation) — safely.

WHY THIS NEEDS CARE: many article titles are mixed Hindi/English. Django's
slugify() strips non-ASCII characters. On an English-heavy title that's
fine. On a Hindi-heavy title it can collapse to something useless (e.g. a
title that's 95% Devanagari can slugify down to just "99"). So this
command NEVER applies a change blindly — it:

  1. Computes a candidate slug from the article's title.
  2. Truncates long candidates at a word boundary (never mid-word).
  3. REFUSES to use the candidate if it's too short/non-descriptive
     (< 8 characters, or purely numeric) — those are left untouched and
     printed as "SKIPPED — needs a manual slug", because guessing wrong
     here is worse than leaving the ugly-but-working slug alone.
  4. Ensures uniqueness against existing slugs (appends -2, -3, ... on
     collision).

DRY RUN BY DEFAULT — shows you the full old -> new table and does nothing.
Only renames when you pass --apply, and only for the specific slugs you
approve via --only (comma-separated old slugs), or --apply-all for every
non-skipped candidate.

No new database migration is introduced: slug stays a normal SlugField
update, and old->new mappings are appended to core/slug_redirects.json
(loaded by core/views.py) so any already-indexed or shared URL still
301-redirects to the new one instead of breaking.

USAGE
  # 1. See what would change (safe, no writes):
  python manage.py regenerate_broken_slugs

  # 2. Apply everything that passed the safety check:
  python manage.py regenerate_broken_slugs --apply-all

  # 3. Or apply only specific ones you've reviewed:
  python manage.py regenerate_broken_slugs --apply --only=-relationship-psychology,Human-Behavior
"""
import json
import os
import re

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Article
from core.views import SLUG_REDIRECTS_PATH


MIN_ACCEPTABLE_LENGTH = 8
MAX_SLUG_LENGTH = 60


def _is_flagged(slug: str) -> bool:
    if slug.startswith('-') or slug.endswith('-'):
        return True
    if slug != slug.lower():
        return True
    if re.search(r'-[a-z]{1,3}$', slug) and len(slug) > 40:
        return True
    return False


def _truncate_at_word_boundary(slug: str, max_len: int) -> str:
    if len(slug) <= max_len:
        return slug
    cut = slug[:max_len].rsplit('-', 1)[0]
    return cut if cut else slug[:max_len]


def _make_unique(candidate: str, taken: set) -> str:
    if candidate not in taken:
        return candidate
    i = 2
    while f"{candidate}-{i}" in taken:
        i += 1
    return f"{candidate}-{i}"


class Command(BaseCommand):
    help = "Safely regenerate broken article slugs (dry-run by default) with 301-redirect tracking."

    def add_arguments(self, parser):
        parser.add_argument('--apply-all', action='store_true',
                             help='Apply every candidate that passes the safety check.')
        parser.add_argument('--apply', action='store_true',
                             help='Apply only the slugs listed in --only.')
        parser.add_argument('--only', type=str, default='',
                             help='Comma-separated list of old slugs to apply (used with --apply).')

    def handle(self, *args, **options):
        apply_all = options['apply_all']
        apply_only = options['apply']
        only_slugs = {s.strip() for s in options['only'].split(',') if s.strip()}

        all_slugs = set(Article.objects.values_list('slug', flat=True))
        flagged = [a for a in Article.objects.all() if _is_flagged(a.slug)]

        if not flagged:
            self.stdout.write(self.style.SUCCESS("No flagged slugs found. Nothing to do."))
            return

        redirects = {}
        if os.path.exists(SLUG_REDIRECTS_PATH):
            with open(SLUG_REDIRECTS_PATH, 'r', encoding='utf-8') as f:
                redirects = json.load(f)

        applied = []
        skipped = []
        taken = set(all_slugs)

        self.stdout.write(f"{'OLD SLUG':<55} {'NEW SLUG':<55} STATUS")
        self.stdout.write("-" * 120)

        for article in flagged:
            raw = slugify(article.title)
            candidate = _truncate_at_word_boundary(raw, MAX_SLUG_LENGTH).strip('-')

            if len(candidate) < MIN_ACCEPTABLE_LENGTH or candidate.isdigit():
                skipped.append(article.slug)
                self.stdout.write(self.style.WARNING(
                    f"{article.slug:<55} {'(none — title too Hindi-heavy)':<55} SKIPPED — needs manual slug"
                ))
                continue

            candidate = _make_unique(candidate, taken - {article.slug})

            should_apply = apply_all or (apply_only and article.slug in only_slugs)

            if should_apply:
                old_slug = article.slug
                article.slug = candidate
                article.save(update_fields=['slug'])
                taken.discard(old_slug)
                taken.add(candidate)
                redirects[old_slug] = candidate
                applied.append((old_slug, candidate))
                self.stdout.write(self.style.SUCCESS(f"{old_slug:<55} {candidate:<55} APPLIED"))
            else:
                self.stdout.write(f"{article.slug:<55} {candidate:<55} (dry run — would apply)")

        if applied:
            with open(SLUG_REDIRECTS_PATH, 'w', encoding='utf-8') as f:
                json.dump(redirects, f, ensure_ascii=False, indent=2)
            self.stdout.write(self.style.SUCCESS(
                f"\nApplied {len(applied)} rename(s) and updated {SLUG_REDIRECTS_PATH}."
            ))
            self.stdout.write(
                "Commit core/slug_redirects.json to git and redeploy so the "
                "redirects take effect in production."
            )
        else:
            self.stdout.write(
                "\nDry run only — no changes made. Re-run with --apply-all "
                "(or --apply --only=slug1,slug2) once you've reviewed the table above."
            )

        if skipped:
            self.stdout.write(self.style.WARNING(
                f"\n{len(skipped)} slug(s) skipped (title is mostly non-Latin script, "
                "auto-slug would be meaningless). Rename these manually in Django admin:"
            ))
            for s in skipped:
                self.stdout.write(f"  - {s}")
