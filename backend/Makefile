# Makefile for UniQuest backend

.PHONY: help install migrate test run clean docker-build docker-run lint format

# Default target
help: ## Show this help message
	@echo "UniQuest Backend - Available Commands:"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development
install: ## Install dependencies
	pip install -r requirements.txt

migrate: ## Run database migrations
	python manage.py makemigrations
	python manage.py migrate

test: ## Run tests
	python manage.py test --settings=uniquest_backend.settings.test

run: ## Run development server
	python manage.py runserver --settings=uniquest_backend.settings.dev

shell: ## Open Django shell
	python manage.py shell --settings=uniquest_backend.settings.dev

# Data ingestion
ingest: ## Download and curate dataset (example)
	python manage.py download_openalex --version 2025.09
	python manage.py load_webometrics --version 2025.09 --csv /data/raw/webometrics/2025.09/webometrics.csv
	python manage.py curate --version 2025.09

activate: ## Activate dataset version
	python manage.py activate --version 2025.09

validate: ## Validate current dataset
	python manage.py validate --verbose

# Docker
docker-build: ## Build Docker image
	docker build -t uniquest-backend .

docker-run: ## Run with Docker Compose
	docker-compose up -d

docker-dev: ## Run development environment with Docker
	docker-compose -f docker-compose.dev.yml up

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f web

# Code quality
lint: ## Run linting
	flake8 .
	mypy .
	bandit -r . -f json -o bandit-report.json

format: ## Format code
	black .
	isort .

# Maintenance
clean: ## Clean up temporary files
	find . -type d -name __pycache__ -delete
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name ".coverage" -delete
	find . -name "*.log" -delete

superuser: ## Create superuser
	python manage.py createsuperuser --settings=uniquest_backend.settings.dev

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

# Database
db-reset: ## Reset database (WARNING: destroys data)
	python manage.py flush --settings=uniquest_backend.settings.dev

db-backup: ## Backup database
	python manage.py dumpdata --settings=uniquest_backend.settings.dev > backup.json

db-restore: ## Restore database from backup
	python manage.py loaddata backup.json --settings=uniquest_backend.settings.dev

# API Documentation
docs: ## Generate API documentation
	python manage.py spectacular --color --file schema.yml
	@echo "API schema generated at schema.yml"
	@echo "View docs at: http://localhost:8000/api/docs/"

# Production
deploy-check: ## Run deployment checks
	python manage.py check --deploy --settings=uniquest_backend.settings.prod

# Sample data
seed: ## Create sample data for development
	python manage.py shell --settings=uniquest_backend.settings.dev -c "
from django.contrib.auth import get_user_model;
from apps.students.models import StudentProfile;
from apps.preferences.models import Preference;
User = get_user_model();
if not User.objects.filter(email='demo@uniquest.com').exists():
    user = User.objects.create_user(
        email='demo@uniquest.com',
        password='demo123',
        username='demo',
        first_name='Demo',
        last_name='User'
    );
    profile = StudentProfile.objects.create(
        user=user,
        gpa=3.5,
        interests='Computer Science, AI, Machine Learning',
        goals='Pursue graduate studies in AI',
        country_preference='US',
        budget_min=20000,
        budget_max=80000
    );
    preferences = Preference.objects.create(user=user);
    print('Demo user created: demo@uniquest.com / demo123');
else:
    print('Demo user already exists');
"
