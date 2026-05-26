from django.contrib import admin
from .models import Article, Subscriber


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'is_published', 'is_featured', 'created_at')
    list_filter   = ('category', 'is_published', 'is_featured')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_featured')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)