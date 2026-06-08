from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from cloudinary_storage.storage import MediaCloudinaryStorage


class Article(models.Model):

    LANGUAGE_CHOICES = [
        ('HI', 'Hindi'),
        ('EN', 'English'),
    ]

    TOPIC_SECTION_CHOICES = [
        ('attachment', 'Attachment Theory'),
        ('validation', 'Validation Psychology'),
        ('dependency', 'Emotional Dependency'),
        ('relationship', 'Relationship Psychology'),
        ('behavior', 'Human Behavior'),
        ('dark', 'Dark Psychology'),
        ('stoicism', 'Stoicism'),
        ('dopamine', 'Dopamine & Modern Mind'),
        ('transformation', 'Self Transformation'),
        ('ai_mind', 'AI & Human Mind'),
    ]

    CATEGORY_CHOICES = [
        ('women',     'Women Psychology'),
        ('dark',      'Dark Psychology'),
        ('breakup',   'Breakup Recovery'),
        ('stoic',     'Stoicism'),
        ('dopamine',  'Dopamine & Modern Mind'),
        ('human',     'Human Behavior'),
        ('transform', 'Self-Transformation'),
        ('aimind',    'AI + Human Mind'),
    ]

    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='HI',
    )

    topic_section = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=TOPIC_SECTION_CHOICES,
    )

    meta_description = models.CharField(
        max_length=160,
        blank=True
    )

    thumbnail = models.ImageField(
        upload_to='thumbs/',
        blank=True,
        null=True,
        storage=MediaCloudinaryStorage()
    )

    content = RichTextField()

    is_published = models.BooleanField(default=True)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def reading_time(self):
        """Estimated reading time in minutes (220 words/min average)."""
        words = len(self.content.split())
        return max(1, round(words / 220))


class Subscriber(models.Model):
    """Newsletter subscribers."""

    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ArticleLink(models.Model):
    LINK_TYPE_CHOICES = [
        ('auto_category', 'Auto: Same Category'),
        ('auto_keyword',  'Auto: Keyword Match'),
        ('manual',        'Manual: Editor Placed'),
        ('pillar',        'Pillar: Category Page Link'),
    ]
    source_article = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        related_name='outbound_links'
    )
    target_article = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        related_name='inbound_links'
    )
    anchor_text    = models.CharField(max_length=200, blank=True)
    link_type      = models.CharField(max_length=20, choices=LINK_TYPE_CHOICES)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    created_by_run = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('source_article', 'target_article')
        indexes = [
            models.Index(fields=['source_article', 'is_active']),
            models.Index(fields=['target_article', 'is_active']),
        ]

    def clean(self):
        if self.source_article_id == self.target_article_id:
            raise ValidationError('Article cannot link to itself.')
        if self.source_article.language != self.target_article.language:
            raise ValidationError(
                f'Cross-language links are prohibited. '
                f'source={self.source_article.language}, '
                f'target={self.target_article.language}'
            )


class ArticleContentBackup(models.Model):
    article       = models.ForeignKey(Article, on_delete=models.CASCADE,
                                       related_name='content_backups')
    content_before = models.TextField()
    run_id         = models.CharField(max_length=100)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['article', 'run_id'])]