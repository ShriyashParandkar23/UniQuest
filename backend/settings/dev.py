"""
Development settings for UniQuest project.

This configuration is used for local development.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Additional allowed hosts for development
ALLOWED_HOSTS += ['0.0.0.0', 'localhost', '127.0.0.1']

# Database - SQLite for both development and production simplicity
# Can be overridden with environment variables if needed
DB_NAME = env('DB_NAME', default='db.sqlite3')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / DB_NAME,
    }
}

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]

# Development-specific middleware
MIDDLEWARE += [
    'django.middleware.common.CommonMiddleware',
]

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable HTTPS-related security in development
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0

# Django Extensions (if installed)
try:
    import django_extensions
    INSTALLED_APPS += ['django_extensions']
except ImportError:
    pass

# Debug Toolbar (if installed)
try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1', '::1']
    
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    }
except ImportError:
    pass

# Development logging
LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['console'],
    'level': 'DEBUG' if env('DEBUG_SQL', default=False) else 'INFO',
    'propagate': False,
}

# Dataset path for development
DATASET_BASE_PATH = env('DATASET_BASE_PATH', default=str(BASE_DIR / 'data'))

# Relaxed rate limiting for development
RATE_LIMIT_ENABLED = env.bool('RATE_LIMIT_ENABLED', default=False)
