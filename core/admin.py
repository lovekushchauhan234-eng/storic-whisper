from django.contrib import admin
from .models import Article, Subscriber


from django.db import models
from django.forms import Textarea

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display  = (
        'title', 'language', 'category', 'topic_section',
        'is_published', 'is_featured', 'created_at',
    )
    list_filter   = ('language', 'category', 'topic_section', 'is_published', 'is_featured')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_featured')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 30, 'cols': 100})},
    }

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)