"""
WSGI config for UniQuest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Determine environment
environment = os.environ.get('DJANGO_ENVIRONMENT', 'dev')

settings_module_map = {
    'dev': 'settings.dev',
    'development': 'settings.dev',
    'prod': 'settings.prod',
    'production': 'settings.prod',
    'test': 'settings.test',
    'testing': 'settings.test',
}

settings_module = settings_module_map.get(
    environment.lower(), 
    'settings.dev'
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()