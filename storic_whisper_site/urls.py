from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from core.sitemaps import StaticSitemap, ArticleSitemap

# ── Sitemap registry ───────────────────────────────────────────
sitemaps = {
    'static':   StaticSitemap,
    'articles': ArticleSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── CKEditor Upload URL ──────────────────────────────────
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # ── Sitemap ──────────────────────────────────────────────
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    # ── Robots.txt ───────────────────────────────────────────
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain',
    )),

    # ── Main app ─────────────────────────────────────────────
    path('', include('core.urls')),
]

# Serve media locally (when DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)