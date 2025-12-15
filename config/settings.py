"""
Django settings for Kaffero Showcase Website.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-6$^1s*=4d5)__p7f2he@@pl@5v^r)d2g4y*0&u^0m6vti9j9^*')

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,.railway.app,kaffero.in,.kaffero.in').split(',')

CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://kaffero.in',
    'https://*.kaffero.in',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Local apps
    'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Whitenoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# Use DATABASE_URL from environment if available (Railway provides this)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise configuration for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
# Use /app/media for Railway volume, fallback to local for development
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', BASE_DIR / 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================================
# SITE SETTINGS (Kaffero)
# =============================================================================

SITE_NAME = 'Kaffero'
SITE_TAGLINE = 'Run Your Cafe Like a Pro'
SITE_DESCRIPTION = 'Complete cafe management system with orders, tables, kitchen display, waiter app, and QR ordering.'

# Company Info
COMPANY_NAME = 'Ralfiz Technologies'
COMPANY_EMAIL = 'hello@kaffero.in'
COMPANY_PHONE = '+91 98956 63498'
COMPANY_WHATSAPP = '+91 98956 63498'
COMPANY_ADDRESS = 'Kerala, India'

# Social Media
SOCIAL_LINKEDIN = 'https://linkedin.com/company/ralfiz'
SOCIAL_INSTAGRAM = 'https://instagram.com/kaffero'
SOCIAL_FACEBOOK = 'https://facebook.com/kaffero'
SOCIAL_YOUTUBE = 'https://youtube.com/@kaffero'


# =============================================================================
# EMAIL SETTINGS
# =============================================================================

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

DEFAULT_FROM_EMAIL = 'Kaffero <hello@kaffero.in>'
ADMIN_EMAIL = 'admin@kaffero.in'


# =============================================================================
# PRICING CONFIGURATION
# =============================================================================

PRICING = {
    'starter': {
        'name': 'Starter',
        'price': 35000,
        'outlets': 1,
        'tables': 5,
        'users': 3,
        'support': '1 year',
        'features': ['Basic features', 'Email support'],
    },
    'standard': {
        'name': 'Standard',
        'price': 65000,
        'outlets': 3,
        'tables': 20,
        'users': 10,
        'support': '1 year',
        'features': ['All features', 'Priority support', 'Setup assistance'],
        'popular': True,
    },
    'premium': {
        'name': 'Premium',
        'price': 95000,
        'outlets': 'Unlimited',
        'tables': 'Unlimited',
        'users': 'Unlimited',
        'support': '1 year',
        'features': ['All features', 'Priority support', 'On-site setup', 'Custom training'],
    },
}

# Annual renewal fee (percentage of license)
RENEWAL_FEE_PERCENT = 20


# =============================================================================
# SECURITY SETTINGS (Production)
# =============================================================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
