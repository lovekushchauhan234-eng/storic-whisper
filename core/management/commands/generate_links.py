from django.core.management.base import BaseCommand
from core.models import Article, ArticleLink
from core.linking.engine import generate_links_for_article, generate_run_id, rollback_run
from django.conf import settings
import os
import dj_database_url


class Command(BaseCommand):
    help = 'Generate internal links between articles'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', default=True)
        parser.add_argument('--write', action='store_true',
                            help='Actually write links (default is dry-run)')
        parser.add_argument('--article', type=str,
                            help='Slug of single article to process')
        parser.add_argument('--language', choices=['HI','EN'],
                            help='Process only one language')
        parser.add_argument('--max-links', type=int, default=3,
                            help='Max internal links to add per article')
        parser.add_argument('--min-score', type=float, default=0.5,
                            help='Minimum quality score to include a link')
        parser.add_argument('--rollback', type=str,
                            help='Rollback all changes from a specific run ID')
        parser.add_argument('--audit', action='store_true',
                            help='Show link health report without modifying anything')
        parser.add_argument('--orphans', action='store_true',
                            help='Show articles with zero inbound links')
        parser.add_argument('--database-url', type=str,
                            help='Temporary override DATABASE_URL for this run (e.g., production database)')

    def handle(self, *args, **options):
        # Handle database URL override
        original_database_url = os.environ.get('DATABASE_URL', '')
        if options['database_url']:
            os.environ['DATABASE_URL'] = options['database_url']
            # Reconfigure database connection
            settings.DATABASES['default'] = dj_database_url.parse(
                options['database_url'],
                conn_max_age=600,
                conn_health_checks=True,
            )
        
        # Handle rollback
        if options['rollback']:
            self.handle_rollback(options['rollback'])
            # Restore original DATABASE_URL
            if original_database_url:
                os.environ['DATABASE_URL'] = original_database_url
            return
        
        # Handle audit
        if options['audit']:
            self.handle_audit()
            # Restore original DATABASE_URL
            if original_database_url:
                os.environ['DATABASE_URL'] = original_database_url
            return
        
        # Handle orphans
        if options['orphans']:
            self.handle_orphans()
            # Restore original DATABASE_URL
            if original_database_url:
                os.environ['DATABASE_URL'] = original_database_url
            return
        
        # Handle link generation
        self.handle_generation(options)
        
        # Restore original DATABASE_URL
        if original_database_url:
            os.environ['DATABASE_URL'] = original_database_url

    def handle_rollback(self, run_id):
        """Rollback all changes from a specific run ID."""
        self.stdout.write(self.style.WARNING(f'Rolling back run: {run_id}'))
        results = rollback_run(run_id)
        
        self.stdout.write(self.style.SUCCESS(f'Articles restored: {results["articles_restored"]}'))
        self.stdout.write(self.style.SUCCESS(f'Links deactivated: {results["links_deactivated"]}'))
        
        if results['errors']:
            self.stdout.write(self.style.ERROR('Errors encountered:'))
            for error in results['errors']:
                self.stdout.write(self.style.ERROR(f'  - {error["article"]}: {error["error"]}'))

    def handle_audit(self):
        """Show link health report."""
        total_articles = Article.objects.filter(is_published=True).count()
        total_links = ArticleLink.objects.filter(is_active=True).count()
        
        self.stdout.write(self.style.SUCCESS('=== LINK AUDIT ==='))
        self.stdout.write(f'Total published articles: {total_articles}')
        self.stdout.write(f'Total active links: {total_links}')
        self.stdout.write(f'Average links per article: {total_links / total_articles if total_articles > 0 else 0:.2f}')
        
        # Check for cross-language links
        cross_language = 0
        for link in ArticleLink.objects.filter(is_active=True):
            if link.source_article.language != link.target_article.language:
                cross_language += 1
        
        if cross_language > 0:
            self.stdout.write(self.style.ERROR(f'Cross-language links found: {cross_language} (SHOULD BE 0)'))
        else:
            self.stdout.write(self.style.SUCCESS('Cross-language links: 0 (CORRECT)'))

    def handle_orphans(self):
        """Show articles with zero inbound links."""
        orphans = []
        for article in Article.objects.filter(is_published=True):
            inbound_count = article.inbound_links.filter(is_active=True).count()
            if inbound_count == 0:
                orphans.append(article)
        
        self.stdout.write(self.style.SUCCESS('=== ORPHAN ARTICLES ==='))
        self.stdout.write(f'Articles with zero inbound links: {len(orphans)}')
        
        for article in orphans:
            self.stdout.write(f'  - {article.title} ({article.slug}) - {article.language}')

    def handle_generation(self, options):
        """Handle link generation."""
        dry_run = options['dry_run']
        if options['write']:
            dry_run = False
        
        run_id = generate_run_id()
        
        self.stdout.write(self.style.SUCCESS('=== GENERATE_LINKS ==='))
        self.stdout.write(f'Mode: {"DRY RUN (no content will be modified)" if dry_run else "WRITE MODE"}')
        self.stdout.write(f'Run ID: {run_id}')
        self.stdout.write(f'Database: {settings.DATABASES["default"]["NAME"]}')
        
        # Diagnostic output
        self.stdout.write(self.style.WARNING('=== DIAGNOSTICS ==='))
        self.stdout.write(f'Model imported: {Article.__module__}.{Article.__name__}')
        self.stdout.write(f'Model table name: {Article._meta.db_table}')
        self.stdout.write(f'Total articles in database: {Article.objects.count()}')
        self.stdout.write(f'Published articles: {Article.objects.filter(is_published=True).count()}')
        
        # Load candidate articles
        articles = Article.objects.filter(is_published=True)
        
        self.stdout.write(f'Queryset after is_published filter: {articles.count()} articles')
        self.stdout.write(f'First 20 article slugs: {list(articles.values_list("slug", flat=True)[:20])}')
        self.stdout.write('')
        
        if options['article']:
            articles = articles.filter(slug=options['article'])
        
        if options['language']:
            articles = articles.filter(language=options['language'])
        
        self.stdout.write(f'Processing {articles.count()} articles (language: {options["language"] or "ALL"})...')
        self.stdout.write('')
        
        total_proposed = 0
        total_skipped_duplicate = 0
        total_skipped_below_score = 0
        total_skipped_injection = 0
        
        for article in articles:
            self.stdout.write(self.style.WARNING(f'--- Article: {article.slug} ({article.language}) ---'))
            
            # Get category/topic for display
            if article.language == 'HI':
                category_info = f'Category: {article.get_category_display()}'
            else:
                category_info = f'Topic: {article.get_topic_section_display() or "None"}'
            
            self.stdout.write(f'  {category_info} | Score threshold: {options["min_score"]}')
            
            results = generate_links_for_article(
                article=article,
                max_links=options['max_links'],
                min_score=options['min_score'],
                dry_run=dry_run,
                run_id=run_id
            )
            
            self.stdout.write(f'  Candidates found: {len(results["proposed_links"]) + len(results["skipped_duplicates"]) + len(results["skipped_below_score"])}')
            
            for link in results['proposed_links']:
                self.stdout.write(self.style.SUCCESS(f'  PROPOSED: {link["target"].slug:<30} score={link["score"]:.2f}'))
                total_proposed += 1
            
            for link in results['skipped_duplicates']:
                self.stdout.write(self.style.WARNING(f'  ALREADY LINKED: {link["target"].slug:<30} [skipped — link exists]'))
                total_skipped_duplicate += 1
            
            for link in results['skipped_below_score']:
                self.stdout.write(self.style.WARNING(f'  SKIPPED: {link["target"].slug:<30} score={link["score"]:.2f} [below min_score]'))
                total_skipped_below_score += 1
            
            for link in results['skipped_injection_failed']:
                self.stdout.write(self.style.ERROR(f'  INJECTION FAILED: {link["target"].slug:<30} [{link["reason"]}]'))
                total_skipped_injection += 1
            
            self.stdout.write('')
        
        # Summary
        self.stdout.write(self.style.SUCCESS('=== SUMMARY ==='))
        self.stdout.write(f'Articles processed: {articles.count()}')
        self.stdout.write(f'Proposed new links: {total_proposed}')
        self.stdout.write(f'Skipped (duplicate): {total_skipped_duplicate}')
        self.stdout.write(f'Skipped (below score): {total_skipped_below_score}')
        self.stdout.write(f'Skipped (injection failed): {total_skipped_injection}')
        
        if dry_run:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('To apply: python manage.py generate_links --write'))
            self.stdout.write(self.style.WARNING(f'Rollback: python manage.py generate_links --rollback {run_id}'))
