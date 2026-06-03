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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'language' in form.base_fields:
            form.base_fields['language'].help_text = 'Select language first. This determines which categorization field to use.'
        if 'category' in form.base_fields:
            form.base_fields['category'].help_text = 'Use this for HINDI articles only (language=HI). Leave blank for English articles.'
        if 'topic_section' in form.base_fields:
            form.base_fields['topic_section'].help_text = 'Use this for ENGLISH articles only (language=EN). Leave blank for Hindi articles.'
        return form

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            ('Basic Information', {
                'fields': ('title', 'slug', 'language'),
                'description': 'Select language first. This determines which categorization field to use below.'
            }),
            ('Hindi Content Categorization', {
                'fields': ('category',),
                'classes': ('collapse',),
                'description': 'Fill this ONLY for Hindi articles (language=HI). Leave blank for English articles.'
            }),
            ('English Content Categorization', {
                'fields': ('topic_section',),
                'classes': ('collapse',),
                'description': 'Fill this ONLY for English articles (language=EN). Leave blank for Hindi articles.'
            }),
            ('Content', {
                'fields': ('meta_description', 'thumbnail', 'content')
            }),
            ('Publishing', {
                'fields': ('is_published', 'is_featured')
            }),
        )
        return fieldsets

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)