from django.db import models


class Article(models.Model):
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

    title            = models.CharField(max_length=200)
    slug             = models.SlugField(unique=True)
    category         = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    meta_description = models.CharField(max_length=160, blank=True)
    thumbnail        = models.ImageField(upload_to='thumbs/', blank=True, null=True)
    content          = models.TextField()
    is_published     = models.BooleanField(default=True)
    is_featured      = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

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
    email      = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email