"""
Production settings for UniQuest project.

This configuration is used for production deployment.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Session security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'

# CSRF security
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'

# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS',
    default=['https://yourdomain.com']
)

# Database - SQLite for production (can be easily migrated to PostgreSQL if needed)
DB_NAME = env('DB_NAME', default='db_production.sqlite3')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / DB_NAME,
        'OPTIONS': {
            'timeout': 20,  # Prevent database locked errors
        },
    }
}

# Static files (use a proper static file server in production)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Email configuration (configure with your email service)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@uniquest.com')

# Caching (use Redis in production)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session store (use Redis in production)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Production logging
LOGGING['handlers']['file'] = {
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': env('LOG_FILE', default='/var/log/uniquest/django.log'),
    'maxBytes': 1024*1024*100,  # 100MB
    'backupCount': 5,
    'formatter': 'json',
}

LOGGING['root']['handlers'] = ['console', 'file']
LOGGING['loggers']['django']['handlers'] = ['console', 'file']
LOGGING['loggers']['apps']['handlers'] = ['console', 'file']

# Error reporting (configure with your error tracking service)
# Example for Sentry:
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# from sentry_sdk.integrations.logging import LoggingIntegration
# 
# sentry_sdk.init(
#     dsn=env('SENTRY_DSN', default=''),
#     integrations=[
#         DjangoIntegration(),
#         LoggingIntegration(level=logging.INFO),
#     ],
#     traces_sample_rate=0.1,
#     send_default_pii=True,
# )

# Rate limiting enabled in production
RATE_LIMIT_ENABLED = True

# Dataset configuration for production
DATASET_BASE_PATH = env('DATASET_BASE_PATH', default='/data')

# Additional security headers
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
