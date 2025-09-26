# UniQuest Backend - Employee Onboarding Guide

Welcome to the UniQuest Backend project! This guide will help you get started with the development environment quickly and smoothly.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.9 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads/)
- **pip** (Python package manager) - Usually comes with Python

### Verify Prerequisites

```bash
# Check Python version
python3 --version  # Should show 3.9 or higher

# Check Git
git --version

# Check pip
pip3 --version
```

## 🚀 Quick Start Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd UniQuest/backend
```

### Step 2: Set Up Python Virtual Environment

**Why Virtual Environment?** It isolates project dependencies and prevents conflicts with other Python projects.

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Your terminal prompt should now show (venv)
```

### Step 3: Install Dependencies

```bash
# Ensure you're in the backend directory and virtual environment is activated
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. **Copy Configuration Template**
   ```bash
   cp config_template.txt .env
   ```

2. **Edit .env File**
   ```bash
   # Use your preferred text editor
   nano .env
   # OR
   vim .env
   # OR open in VS Code
   code .env
   ```

3. **Update Configuration**
   ```env
   # Generate a new secret key using: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   SECRET_KEY=your-generated-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # SQLite database is used by default (no additional configuration needed)
   # Database file will be created automatically as 'db.sqlite3' in the backend directory
   ```

### Step 5: Run Database Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database (creates db.sqlite3 file automatically)
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser

# Follow prompts to set:
# - Username: admin
# - Email address: admin@uniquest.com
# - Password: admin2025
# - Confirm password: admin2025
```

**📝 Django Admin Credentials:**
- **URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin2025`

> **Note**: These are development credentials. Use strong, unique credentials in production.

### Step 7: Start Development Server

```bash
python manage.py runserver

# Server will start at: http://127.0.0.1:8000/
```

## ✅ Verify Installation

### 1. Check Health Endpoint
Open your browser and visit: `http://127.0.0.1:8000/api/health/`

You should see:
```json
{
  "status": "healthy",
  "message": "UniQuest Backend is running!"
}
```

### 2. Access Django Admin
Visit: `http://127.0.0.1:8000/admin/`
Log in with the superuser credentials you created.

## 📁 Project Structure

```
backend/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── config_template.txt       # Environment variables template
├── .env                      # Environment variables (you create this)
├── db.sqlite3               # SQLite database (created automatically)
├── README.md                # This file
├── uniquest_backend/        # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
└── venv/                    # Virtual environment (created by you)
```

## 🔧 Development Workflow

### Daily Development Routine

1. **Activate Virtual Environment**
   ```bash
   cd UniQuest/backend
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate   # On Windows
   ```

2. **Pull Latest Changes**
   ```bash
   git pull origin main
   ```

3. **Install New Dependencies** (if requirements.txt changed)
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations** (if models changed)
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

### Creating New Django Apps

```bash
# Create a new Django app
python manage.py startapp app_name

# Don't forget to add it to INSTALLED_APPS in settings.py
```

### Database Operations

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (careful - this deletes all data!)
python manage.py flush

# Create database backup
cp db.sqlite3 db_backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Restore database backup
cp db_backup_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test app_name

# Run with coverage (install coverage first: pip install coverage)
coverage run --source='.' manage.py test
coverage report
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. "ModuleNotFoundError: No module named 'django'"
**Solution:** Activate your virtual environment
```bash
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

#### 2. "Port 8000 is already in use"
**Solution:** Use a different port
```bash
python manage.py runserver 8001
```

#### 3. "django.db.utils.OperationalError: database is locked"
**Solution:** 
```bash
# Close any open database connections
# Make sure no other Django processes are running
ps aux | grep manage.py
# Kill any running processes if found
```

#### 4. Migration Issues
**Solution:** 
```bash
# Delete migration files (keep __init__.py)
# Reset migrations
python manage.py makemigrations --empty app_name
python manage.py migrate --fake-initial
```

#### 5. "SECRET_KEY" not found error
**Solution:** 
```bash
# Make sure .env file exists and contains SECRET_KEY
# Generate a new secret key:
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
# Add it to your .env file
```

### Development Tools

```bash
# Check for issues
python manage.py check

# Shell with Django context
python manage.py shell

# Collect static files
python manage.py collectstatic

# Create database dump
python manage.py dumpdata > data_backup.json

# Load database dump
python manage.py loaddata data_backup.json
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)

## 🤝 Getting Help

If you encounter issues during setup:

1. **Check this README** - Most common issues are covered here
2. **Ask Team Members** - Don't hesitate to reach out
3. **Create GitHub Issue** - For bugs or feature requests
4. **Check Django Documentation** - For deeper technical issues

## 🔐 Security Notes

- **Never commit .env files** - They contain sensitive information
- **Use strong passwords** - For admin accounts  
- **Keep dependencies updated** - Run `pip list --outdated` regularly
- **Use HTTPS in production** - This setup is for development only

## 🎯 Why SQLite?

**SQLite Benefits:**
- ✅ **Zero Configuration** - No database server setup required
- ✅ **File-based** - Easy to backup and move
- ✅ **Fast** - Excellent performance for most applications
- ✅ **Reliable** - ACID-compliant, battle-tested
- ✅ **Cross-platform** - Works on all operating systems
- ✅ **Perfect for Development** - Start coding immediately
- ✅ **Production Ready** - Handles most real-world applications

**When to consider alternatives:**
- High concurrency (1000+ simultaneous users)
- Multiple applications accessing same database
- Large datasets (100GB+)
- Complex analytical queries

For most applications, SQLite is the perfect choice!

---

**🎉 Congratulations!** You should now have a fully functional UniQuest backend development environment.

Happy coding! 🚀