"""
Django settings for storic_whisper_site project.
"""

from pathlib import Path
import os
import dj_database_url

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY from environment variable with fallback for local dev
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-!^m22-l+dh2-ijlta!65_t4=ym(cu35u*eyyt+rqmtizox+f*6')

# Render पर DEBUG=False, locally DEBUG=True
DEBUG = os.environ.get('RENDER') is None

# ALLOWED_HOSTS from environment variable with fallback
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
# Ensure each host is stripped of whitespace
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'ckeditor',
    'ckeditor_uploader',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'storic_whisper_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'storic_whisper_site.wsgi.application'

# ── Database ────────────────────────────────────────────────────
# Render पर DATABASE_URL environment variable automatically set होती है
# Locally SQLite use होगा
DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()

if DATABASE_URL:
    try:
        # Render PostgreSQL
        DATABASES = {
            'default': dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    except Exception as e:
        # Fallback to SQLite if DATABASE_URL is invalid
        print(f"Warning: Failed to parse DATABASE_URL: {e}. Falling back to SQLite.")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Local development — SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Cache (Redis on Render, local memory fallback) ─────────────
REDIS_URL = os.environ.get('REDIS_URL', '').strip()

if REDIS_URL:
    try:
        # Render Redis
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                'LOCATION': REDIS_URL,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                },
                'KEY_PREFIX': 'luppi',
                'TIMEOUT': 600,  # 10 minutes default
            }
        }
    except Exception as e:
        # Fallback to local memory cache if Redis fails
        print(f"Warning: Failed to configure Redis: {e}. Falling back to local memory cache.")
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'luppi-cache',
            }
        }
else:
    # Local development — memory cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'luppi-cache',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ── Static Files ────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Media / Cloudinary ──────────────────────────────────────────
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dqhptutne',
    'API_KEY':    '532347431663133',
    'API_SECRET': 'v_Ifw51Z6WiYIJMSegqJ6Ahct2o',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── LUPPI AI ────────────────────────────────────────────────────
LUPPI_PROVIDER          = 'gemini'  # Options: 'local', 'anthropic', 'gemini'
LUPPI_SESSION_MAX_TURNS = 24
ANTHROPIC_API_KEY       = os.environ.get('ANTHROPIC_API_KEY', None)  # Set to enable Claude integration
GEMINI_API_KEY          = os.environ.get('GEMINI_API_KEY', None)  # Set to enable Gemini integration
GEMINI_MODEL            = 'gemini-2.5-flash'  # Options: 'gemini-2.5-flash', 'gemini-2.5-pro'
GEMINI_CACHE_TIMEOUT    = 600  # Cache responses for 10 minutes (increased for production)

# ── Production Security Settings ────────────────────────────────
if not DEBUG:
    # CSRF Trusted Origins for production - must include scheme (http:// or https://)
    # Note: Django does NOT support wildcards in CSRF_TRUSTED_ORIGINS
    # Use exact domain names only
    csrf_origins_env = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
    CSRF_TRUSTED_ORIGINS = []
    
    if csrf_origins_env and csrf_origins_env.strip():
        for origin in csrf_origins_env.split(','):
            origin = origin.strip()
            if origin:
                # Ensure scheme is present
                if not origin.startswith(('http://', 'https://')):
                    origin = f'https://{origin}'
                # Only add if not empty after processing
                if origin:
                    CSRF_TRUSTED_ORIGINS.append(origin)
    
    # Session Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # SSL Redirect
    SECURE_SSL_REDIRECT = True
else:
    CSRF_TRUSTED_ORIGINS = []
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SECURE = False
    CSRF_COOKIE_HTTPONLY = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_SSL_REDIRECT = False
# CKEditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': 'uploadimage,image2',
    }
}