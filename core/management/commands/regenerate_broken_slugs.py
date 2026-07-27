"""
Fixes the broken/ugly slugs flagged by `fix_adsense_trust_issues` (leading
hyphens, uppercase, mid-word truncation) — safely.

DB CONSTRAINT: Article.slug is CharField(max_length=50). This command
never generates or writes a slug longer than 50 characters, and it is
NEVER changing that column length. Every candidate is built by joining
whole words only — never by slicing a word in half.

WHY THIS NEEDS CARE: many article titles are mixed Hindi/English. Django's
slugify() strips non-ASCII characters. On an English-heavy title that's
fine. On a Hindi-heavy title it can collapse to something useless (e.g. a
title that's 95% Devanagari can slugify down to just "99"). So this
command NEVER applies a change blindly — it:

  1. Slugifies the title, then removes common English stop words first
     (the, a, of, what, is, ...) so the 50-char budget is spent on
     meaningful/SEO-relevant words rather than filler.
  2. Greedily joins whole words, left to right, stopping BEFORE the next
     word would push the result past 50 characters. Never cuts a word.
  3. If stop-word removal + word-boundary joining still yields something
     too short/non-descriptive (< 8 characters, or purely numeric), the
     article is SKIPPED and left untouched — printed as "needs a manual
     slug" — because guessing wrong is worse than leaving the ugly-but-
     working slug alone.
  4. Ensures uniqueness against existing slugs (appends -2, -3, ...),
     shrinking the base further if needed so the suffixed slug still
     fits in 50 characters.

DRY RUN BY DEFAULT — shows the full old -> new table and writes nothing.
Only renames when you pass --apply-all, or --apply --only=<comma list>.

No new database migration: slug stays a normal SlugField update, and
old->new mappings are appended to core/slug_redirects.json (loaded by
core/views.py's article_detail view) so any already-indexed or shared
URL still 301-redirects to the new one instead of breaking. This
behavior is unchanged from before.

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


# Matches the real DB column: Article.slug = CharField(max_length=50).
# Do not raise this — the command must always produce slugs that fit.
MAX_SLUG_LENGTH = 50
MIN_ACCEPTABLE_LENGTH = 8

STOP_WORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'of', 'and', 'or', 'but', 'to', 'in', 'on', 'at', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before',
    'after', 'above', 'below', 'from', 'up', 'down', 'out', 'off', 'over',
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
    'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should',
    'now', 'this', 'that', 'these', 'those', 'you', 'your', 'yours',
    'it', 'its', 'what', 'which', 'who', 'whom', 'does', 'do', 'did',
}


def _is_flagged(slug: str) -> bool:
    if slug.startswith('-') or slug.endswith('-'):
        return True
    if slug != slug.lower():
        return True
    if re.search(r'-[a-z]{1,3}$', slug) and len(slug) > 40:
        return True
    if len(slug) > MAX_SLUG_LENGTH:
        return True
    return False


def _join_within_limit(words, max_len):
    """
    Greedily join whole words with '-' left to right, stopping BEFORE the
    next word would push the result past max_len. Never slices a word.
    Returns '' if even the first word alone exceeds max_len.
    """
    if not words:
        return ''
    if len(words[0]) > max_len:
        return ''  # caller falls back / skips — we never cut a word

    result = words[0]
    for word in words[1:]:
        candidate = f"{result}-{word}"
        if len(candidate) > max_len:
            break
        result = candidate
    return result


def _build_candidate(title: str, max_len: int) -> str:
    raw = slugify(title)
    if not raw:
        return ''

    all_words = raw.split('-')
    all_words = [w for w in all_words if w]  # drop empty tokens

    # 1st attempt: stop words removed, so the character budget goes to
    # meaningful/SEO-relevant words.
    meaningful_words = [w for w in all_words if w not in STOP_WORDS]
    if not meaningful_words:
        meaningful_words = all_words  # title was ~all stop words; fall back

    candidate = _join_within_limit(meaningful_words, max_len)

    # If that produced nothing usable (e.g. the very first meaningful word
    # alone is longer than max_len), fall back to the full word list —
    # still word-boundary-safe, just without stop-word trimming.
    if len(candidate) < MIN_ACCEPTABLE_LENGTH:
        candidate = _join_within_limit(all_words, max_len)

    return candidate.strip('-')


def _make_unique(candidate: str, taken: set, max_len: int) -> str:
    if candidate not in taken and len(candidate) <= max_len:
        return candidate
    i = 2
    while True:
        suffix = f"-{i}"
        allowed = max_len - len(suffix)
        base = candidate[:allowed].rstrip('-') if allowed > 0 else candidate[:1]
        if not base:
            base = candidate[:max(1, max_len - len(suffix))]
        cand = f"{base}{suffix}"
        if cand not in taken and len(cand) <= max_len:
            return cand
        i += 1


class Command(BaseCommand):
    help = "Safely regenerate broken article slugs (dry-run by default), capped at 50 chars, with 301-redirect tracking."

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

        self.stdout.write(f"{'OLD SLUG':<55} {'NEW SLUG (<=50 chars)':<55} STATUS")
        self.stdout.write("-" * 130)

        for article in flagged:
            candidate = _build_candidate(article.title, MAX_SLUG_LENGTH)

            if len(candidate) < MIN_ACCEPTABLE_LENGTH or candidate.isdigit():
                skipped.append(article.slug)
                self.stdout.write(self.style.WARNING(
                    f"{article.slug:<55} {'(none — title too Hindi-heavy)':<55} SKIPPED — needs manual slug"
                ))
                continue

            candidate = _make_unique(candidate, taken - {article.slug}, MAX_SLUG_LENGTH)
            assert len(candidate) <= MAX_SLUG_LENGTH, "safety check: never exceed the DB column length"

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
