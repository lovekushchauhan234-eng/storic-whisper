from django.db import models
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