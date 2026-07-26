"""
One-time cleanup command for the AdSense re-application pass.

Run this against your PRODUCTION (Supabase) database, e.g.:
    python manage.py fix_adsense_trust_issues

What it does:
1. If no article is currently marked is_featured=True, marks the 3 deepest
   (longest, by computed reading_time) published Hindi articles as
   featured, so the homepage "Start Here / Cornerstone" section stops
   relying on the fallback and shows genuinely curated picks.
   NOTE: reading_time is a plain Python method on the model (derived from
   `content` word count) — it is NOT a database column. It cannot be used
   in .order_by(), so this command pulls the queryset into Python and
   sorts there instead. No migration is needed; only real model fields
   (is_featured, is_published, language, slug) are queried via the ORM.
2. Prints an audit list of slugs that look auto-generated/broken (leading
   hyphen, truncated, or inconsistent casing) so you can review and rename
   them by hand — this command does NOT rename slugs automatically, since
   renaming without a matching redirect breaks any already-indexed URLs.
"""
import re

from django.core.management.base import BaseCommand
from core.models import Article


class Command(BaseCommand):
    help = "Audit and fix low-effort AdSense trust issues (cornerstone flag, slug hygiene)."

    def handle(self, *args, **options):
        hindi_qs = Article.objects.filter(is_published=True, language='HI')

        # 1. Cornerstone / featured articles
        featured_count = hindi_qs.filter(is_featured=True).count()
        if featured_count == 0:
            # reading_time() is a Python method, not a DB field — order_by()
            # can't touch it, so sort in Python after fetching.
            all_articles = list(hindi_qs)
            all_articles.sort(key=lambda a: a.reading_time(), reverse=True)
            candidates = all_articles[:3]

            for article in candidates:
                article.is_featured = True
                article.save(update_fields=['is_featured'])

            self.stdout.write(self.style.SUCCESS(
                f"Marked {len(candidates)} article(s) as is_featured=True: "
                + ", ".join(a.slug for a in candidates)
            ))
        else:
            self.stdout.write(self.style.NOTICE(
                f"{featured_count} article(s) already marked is_featured=True — no change made."
            ))

        # 2. Slug hygiene audit (report only — do not auto-rename)
        self.stdout.write("\n--- Slug hygiene audit (review manually) ---")
        problems_found = False
        for article in Article.objects.all().order_by('slug'):
            slug = article.slug
            issues = []
            if slug.startswith('-') or slug.endswith('-'):
                issues.append("leading/trailing hyphen")
            if slug != slug.lower():
                issues.append("uppercase characters")
            if re.search(r'-[a-z]{1,3}$', slug) and len(slug) > 40:
                issues.append("possibly truncated mid-word")
            if issues:
                problems_found = True
                self.stdout.write(
                    self.style.WARNING(f"  /{slug}/  ->  {', '.join(issues)}")
                )
        if not problems_found:
            self.stdout.write(self.style.SUCCESS("  No slug issues detected."))
        else:
            self.stdout.write(
                "\nTo fix: rename the slug in Django admin AND add a 301 redirect "
                "from the old URL to the new one (see core/urls.py) so any already-"
                "indexed link or shared URL doesn't break."
            )
