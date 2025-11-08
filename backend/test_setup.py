#!/usr/bin/env python
"""
Test script to verify Django setup is working correctly.
Run this after following the README setup instructions.
"""

import os
import sys
import django
from pathlib import Path

def test_django_setup():
    """Test if Django is set up correctly."""
    print("🔍 Testing Django Setup...")
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniquest_backend.settings')
    
    try:
        # Initialize Django
        django.setup()
        print("✅ Django setup successful!")
        
        # Test imports
        from django.core.management import execute_from_command_line
        from django.conf import settings
        print("✅ Django imports working!")
        
        # Test database configuration
        db_config = settings.DATABASES['default']
        print(f"✅ Database configured: {db_config['ENGINE']}")
        print(f"   - Database file: {db_config['NAME']}")
        
        # Check if SQLite database exists
        if Path(db_config['NAME']).exists():
            print("✅ SQLite database file exists")
        else:
            print("⚠️  SQLite database file not found (run 'python manage.py migrate' to create)")
        
        # Test installed apps
        print(f"✅ Installed apps ({len(settings.INSTALLED_APPS)}):")
        for app in settings.INSTALLED_APPS:
            print(f"   - {app}")
        
        # Test middleware
        print(f"✅ Middleware configured ({len(settings.MIDDLEWARE)} items)")
        
        print("\n🎉 Django setup verification completed successfully!")
        print("\n📝 Next steps:")
        print("1. Set up your .env file using config_template.txt")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py createsuperuser")
        print("4. Run: python manage.py runserver")
        
        return True
        
    except ImportError as e:
        print(f"❌ Django import error: {e}")
        print("💡 Solution: Make sure you've activated your virtual environment and installed requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def check_requirements():
    """Check if requirements are available."""
    print("\n🔍 Checking Required Packages...")
    
    required_packages = [
        'django',
        'djangorestframework',
        'django-cors-headers',
        'python-decouple',
        'gunicorn',
        'PIL'  # Pillow
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'django-cors-headers':
                import corsheaders
            elif package == 'djangorestframework':
                import rest_framework
            elif package == 'python-decouple':
                import decouple
            elif package == 'PIL':
                import PIL
            else:
                __import__(package)
            print(f"✅ {package} - installed")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Install missing packages: pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed!")
    return True

def check_file_structure():
    """Check if all necessary files are present."""
    print("\n🔍 Checking File Structure...")
    
    required_files = [
        'manage.py',
        'requirements.txt',
        'uniquest_backend/__init__.py',
        'uniquest_backend/settings.py',
        'uniquest_backend/urls.py',
        'uniquest_backend/wsgi.py',
        'uniquest_backend/asgi.py',
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files are present!")
    return True

if __name__ == '__main__':
    print("🚀 UniQuest Backend Setup Verification")
    print("=" * 50)
    
    # Check file structure
    files_ok = check_file_structure()
    
    # Check requirements
    packages_ok = check_requirements()
    
    # Test Django setup
    if files_ok and packages_ok:
        django_ok = test_django_setup()
        
        if django_ok:
            print("\n🎉 SETUP VERIFICATION PASSED!")
            print("Your Django backend is ready for development!")
        else:
            print("\n❌ SETUP VERIFICATION FAILED!")
            print("Please check the errors above and fix them.")
            sys.exit(1)
    else:
        print("\n❌ SETUP VERIFICATION FAILED!")
        print("Please fix the missing files/packages first.")
        sys.exit(1)
