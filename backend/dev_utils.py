#!/usr/bin/env python
"""
Development utilities for UniQuest Backend.
Helpful commands for common development tasks.
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a shell command and print the result."""
    print(f"🔄 {description}")
    print(f"Running: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Success!")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ Failed!")
        if result.stderr:
            print(result.stderr)
    
    return result.returncode == 0

def setup_database():
    """Set up the database with migrations."""
    print("🗄️ Setting up database...")
    
    # Create migrations
    success = run_command("python manage.py makemigrations", "Creating migrations")
    
    if success:
        # Apply migrations
        success = run_command("python manage.py migrate", "Applying migrations")
    
    return success

def create_superuser():
    """Create a superuser account."""
    print("👤 Creating superuser account...")
    run_command("python manage.py createsuperuser", "Creating superuser")

def collect_static():
    """Collect static files."""
    print("📁 Collecting static files...")
    run_command("python manage.py collectstatic --noinput", "Collecting static files")

def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    run_command("python manage.py test", "Running test suite")

def check_deployment():
    """Check if the project is ready for deployment."""
    print("🔍 Checking deployment readiness...")
    run_command("python manage.py check --deploy", "Deployment check")

def start_server():
    """Start the development server."""
    print("🚀 Starting development server...")
    print("Server will be available at: http://127.0.0.1:8000/")
    print("Press Ctrl+C to stop the server")
    os.system("python manage.py runserver")

def show_urls():
    """Show all available URLs."""
    print("🗺️ Available URLs:")
    run_command("python manage.py show_urls", "Listing URLs")

def shell():
    """Open Django shell."""
    print("🐍 Opening Django shell...")
    os.system("python manage.py shell")

def backup_database():
    """Create a backup of the SQLite database."""
    print("💾 Creating database backup...")
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"db_backup_{timestamp}.sqlite3"
    
    try:
        shutil.copy2("db.sqlite3", backup_name)
        print(f"✅ Database backed up to: {backup_name}")
    except FileNotFoundError:
        print("❌ Database file not found. Run migrations first.")
    except Exception as e:
        print(f"❌ Backup failed: {e}")

def restore_database():
    """Restore database from backup."""
    print("🔄 Available backups:")
    import glob
    backups = glob.glob("db_backup_*.sqlite3")
    
    if not backups:
        print("❌ No backup files found")
        return
    
    for i, backup in enumerate(backups, 1):
        print(f"  {i}. {backup}")
    
    try:
        choice = int(input("Enter backup number to restore: ")) - 1
        if 0 <= choice < len(backups):
            import shutil
            shutil.copy2(backups[choice], "db.sqlite3")
            print(f"✅ Database restored from: {backups[choice]}")
        else:
            print("❌ Invalid choice")
    except (ValueError, KeyboardInterrupt):
        print("❌ Restore cancelled")

def show_help():
    """Show available commands."""
    print("🛠️ UniQuest Backend Development Utilities")
    print("=" * 50)
    print("Available commands:")
    print("  setup      - Set up database with migrations")
    print("  superuser  - Create superuser account")
    print("  static     - Collect static files")
    print("  test       - Run test suite")
    print("  check      - Check deployment readiness")
    print("  server     - Start development server")
    print("  urls       - Show available URLs")
    print("  shell      - Open Django shell")
    print("  backup     - Backup SQLite database")
    print("  restore    - Restore database from backup")
    print("  help       - Show this help message")
    print("")
    print("Usage: python dev_utils.py <command>")

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'setup': setup_database,
        'superuser': create_superuser,
        'static': collect_static,
        'test': run_tests,
        'check': check_deployment,
        'server': start_server,
        'urls': show_urls,
        'shell': shell,
        'backup': backup_database,
        'restore': restore_database,
        'help': show_help,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == '__main__':
    main()
