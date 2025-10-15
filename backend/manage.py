#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Determine which settings to use based on environment
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
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
