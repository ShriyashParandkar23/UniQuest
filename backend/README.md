# UniQuest Backend

A Django 5 + DRF backend for university recommendation system with hybrid architecture - SQLite for transactional data and file-backed datasets (Parquet/CSV) for university data.

## 🏗️ Architecture

- **Transactional Data**: SQLite for users, profiles, preferences, recommendations, and feedback
- **University Dataset**: File-backed Parquet/CSV with DuckDB + Polars for fast queries
- **Data Sources**: Kaggle datasets for universities + optional Webometrics rankings
- **Authentication**: JWT with djangorestframework-simplejwt
- **API Documentation**: OpenAPI 3.0 with drf-spectacular

## 📋 Prerequisites

- Python 3.11+
- Git
- Node.js 18+ (for frontend development)

## ⚡ Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd UniQuest/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
cp env.example .env
# Edit .env if needed (SQLite uses default db.sqlite3)
```

### 5. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Create Demo Data (Optional)

```bash
python manage.py shell < create_demo_data.py
# Creates demo users: alice@example.com, bob@example.com, carol@example.com
# Password for all: demo123
```

## 🚀 Local Development Server

### Option 1: Native Python Server

1. **Start the development server**:
   ```bash
   python manage.py runserver
   # Or use the Makefile
   make run
   ```

2. **Access the application**:
   - **API Docs**: http://localhost:8000/api/docs/
   - **Admin Panel**: http://localhost:8000/admin/
   - **Health Check**: http://localhost:8000/api/healthz/

3. **Development workflow**:
   ```bash
   # Code formatting
   make format
   
   # Linting
   make lint
   
   # Run tests
   make test
   
   # Reset database (development only)
   make db-reset
   
   # Apply migrations
   make migrate
   ```

### Option 2: Docker Development

1. **Start with Docker Compose**:
   ```bash
   make docker-dev
   # Or manually:
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Initialize database in Docker**:
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
   docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
   ```

3. **View logs**:
   ```bash
   docker-compose -f docker-compose.dev.yml logs -f web
   ```

4. **Stop services**:
   ```bash
   docker-compose -f docker-compose.dev.yml down
   ```

### Development Database Management

```bash
# Apply new migrations
make migrate

# Create demo data
make seed

# Reset database (WARNING: destroys all data)
make db-reset

# Backup database
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json
```

## 🏭 Production Server Setup

### Option 1: Docker Production Deployment

1. **Prepare environment**:
   ```bash
   # Copy and configure production environment
   cp env.example .env
   
   # Edit .env with production values:
   # - Set DEBUG=False
   # - Set proper SECRET_KEY
   # - Set ALLOWED_HOSTS
   # - Set DB_NAME=db_production.sqlite3
   ```

2. **Build and deploy**:
   ```bash
   # Build production image
   make docker-build
   
   # Start production services
   docker-compose up -d
   ```

3. **Initialize production database**:
   ```bash
   # Run migrations
   docker-compose exec web python manage.py migrate
   
   # Create superuser
   docker-compose exec web python manage.py createsuperuser
   
   # Collect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

4. **Production maintenance**:
   ```bash
   # View logs
   docker-compose logs -f web
   
   # Restart services
   docker-compose restart
   
   # Stop services
   docker-compose down
   
   # Backup database
   docker-compose exec web python manage.py dumpdata > backup_$(date +%Y%m%d).json
   ```

### Option 2: Manual Production Deployment

1. **Server setup**:
   ```bash
   # Install Python 3.11+ on your server
   # Clone repository
   git clone <repository-url>
   cd UniQuest/backend
   
   # Create production environment
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   # Set production environment variables
   export DJANGO_ENVIRONMENT=prod
   export DEBUG=False
   export SECRET_KEY=your-very-secret-key
   export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   export DB_NAME=db_production.sqlite3
   ```

3. **Initialize production database**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

4. **Start with Gunicorn**:
   ```bash
   # Install Gunicorn (already in requirements.txt)
   gunicorn --bind 0.0.0.0:8000 --workers 4 uniquest_backend.wsgi:application
   
   # Or use systemd service (recommended)
   # Create /etc/systemd/system/uniquest.service
   ```

5. **Nginx Configuration** (recommended):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /static/ {
           alias /path/to/UniQuest/backend/staticfiles/;
       }
       
       location /media/ {
           alias /path/to/UniQuest/backend/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Production Monitoring

1. **Health checks**:
   ```bash
   curl https://yourdomain.com/api/healthz/
   ```

2. **Log monitoring**:
   ```bash
   # View application logs
   tail -f /var/log/uniquest/django.log
   
   # Or with Docker
   docker-compose logs -f web
   ```

3. **Database maintenance**:
   ```bash
   # Regular backups (add to cron)
   python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json
   
   # Database optimization (SQLite)
   python manage.py dbshell
   VACUUM;
   ANALYZE;
   ```

## 📊 Dataset Management

### Data Ingestion Pipeline

#### Setting Up Kaggle Dataset Access

1. **Create Kaggle Account**: Sign up at [kaggle.com](https://www.kaggle.com/)

2. **Get Kaggle API Credentials**:
   - Go to Kaggle Account Settings
   - Click "Create New API Token"
   - Download `kaggle.json` file

3. **Set Environment Variables**:
   ```bash
   export KAGGLE_USERNAME=your_username
   export KAGGLE_KEY=your_api_key
   ```

#### Download University Dataset

1. **Download Kaggle dataset**:
   ```bash
   python manage.py download_dataset --version 2025.09 --kaggle-dataset "username/dataset-name"
   ```
   
   **Example university datasets on Kaggle**:
   - `mylesoneill/world-university-rankings`
   - `theriley106/university-statistics`
   - `imtkaggleteam/global-university-ranking`

2. **Load Webometrics rankings** (optional):
   ```bash
   python manage.py load_webometrics --version 2025.09 --csv /path/to/webometrics.csv
   ```

3. **Curate and merge datasets**:
   ```bash
   python manage.py curate --version 2025.09
   ```

4. **Activate dataset version**:
   ```bash
   python manage.py activate --version 2025.09
   ```

5. **Validate dataset**:
   ```bash
   python manage.py validate --version 2025.09 --verbose
   ```

### Dataset Structure

```
/data/
├── raw/
│   ├── openalex/2025.09/institutions.jsonl
│   └── webometrics/2025.09/webometrics.jsonl
├── curated/
│   └── 2025.09/
│       ├── institutions.parquet
│       └── search_index.parquet
└── current -> 2025.09
```

### Quick Dataset Setup

```bash
# Complete ingestion pipeline
make ingest

# Activate latest version
make activate

# Validate dataset
make validate
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login/` - Login (JWT)
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/verify/` - Verify token

### Student Profiles
- `GET /api/students/me/` - Get profile
- `PATCH /api/students/me/` - Update profile

### Preferences
- `GET /api/students/preferences/` - Get preferences
- `PUT /api/students/preferences/` - Update preferences

### Universities (Dataset-backed)
- `GET /api/universities/?q=stanford&country=US` - Search universities
- `GET /api/universities/{openalex_id}/` - University details

### Recommendations (Hybrid)
- `POST /api/recommendations/run/` - Generate recommendations
- `GET /api/recommendations/` - List user's recommendations

### Feedback
- `POST /api/feedback/recommendations/{id}/` - Provide feedback
- `GET /api/feedback/` - List user's feedback

### System
- `GET /api/healthz/` - Health check
- `GET /api/ingestion/runs/` - Ingestion history

### API Documentation
- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc UI
- `GET /api/schema/` - OpenAPI schema

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific app tests
python manage.py test apps.students --settings=uniquest_backend.settings.test

# Run with coverage
coverage run --source='.' manage.py test --settings=uniquest_backend.settings.test
coverage report
```

## 🏗️ Project Structure

```
backend/
├── apps/
│   ├── users/              # User authentication
│   ├── students/           # Student profiles
│   ├── preferences/        # User preferences
│   ├── recommendations/    # Hybrid recommendations
│   ├── feedback/          # Recommendation feedback
│   └── dataset/           # Dataset management & university search
├── uniquest_backend/
│   ├── settings/          # Environment-specific settings
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
│   │   └── test.py
│   ├── urls.py
│   └── exceptions.py      # Custom error handling
├── db/                    # SQLite database files
├── data/                  # Dataset storage
├── tests/                 # Test utilities and fixtures
├── docker-compose.yml     # Production Docker setup
├── docker-compose.dev.yml # Development Docker setup
├── Dockerfile
├── Makefile              # Development commands
└── requirements.txt
```

## 🔧 Environment Configuration

### Development (.env)
```bash
SECRET_KEY=django-insecure-dev-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=db.sqlite3
DATASET_BASE_PATH=./data

# Kaggle API credentials (for dataset downloads)
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

### Production (.env)
```bash
SECRET_KEY=your-very-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=db_production.sqlite3
DATASET_BASE_PATH=/data
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Kaggle API credentials (for dataset downloads)
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

## 📈 Monitoring & Maintenance

### Health Monitoring
- **Health endpoint**: `GET /api/healthz/`
- **Database status**: Included in health check
- **Dataset status**: Validates current dataset version
- **Ingestion history**: Track all data processing runs

### Regular Maintenance Tasks
```bash
# Database backup (daily)
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Log rotation (configure with logrotate)
# Dataset validation (weekly)
python manage.py validate --verbose

# Static file updates
python manage.py collectstatic --noinput
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Run `make lint` and `make test`
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## 🆘 Support & Troubleshooting

### Common Issues

1. **Database locked error**:
   ```bash
   # Stop all processes accessing the database
   # Or increase timeout in production settings
   ```

2. **Permission errors**:
   ```bash
   # Ensure proper file permissions
   chmod 755 db/
   chmod 644 db/*.sqlite3
   ```

3. **Dataset not found**:
   ```bash
   # Check dataset path and run validation
   python manage.py validate --verbose
   ```

### Support Links
- **API Documentation**: http://localhost:8000/api/docs/
- **Health Check**: http://localhost:8000/api/healthz/
- **Admin Panel**: http://localhost:8000/admin/

For issues and questions, please use the GitHub issue tracker.