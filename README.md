# UniQuest

The project aims to develop a platform that assists students in identifying suitable universities based on their academic profiles, interests, and career aspirations. The system will leverage AI-driven recommendations to provide accurate and personalized suggestions.

## 📚 Documentation

- **[Backend API Documentation](backend/README.md)** - Complete backend setup and development guide
- **[API Endpoints](docs/apis/)** - Postman collection and API reference
- **[User Journey](docs/user_journey.md)** - Detailed user flow and features
- **[UML Diagrams](docs/diagrams/)** - System architecture diagrams

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Test API with Postman
1. Import `docs/apis/UniQuest_API.postman_collection.json`
2. Import `docs/apis/UniQuest_Development.postman_environment.json`
3. Select "UniQuest Development" environment
4. Run Authentication → Login
5. Start testing!

## 🎯 Key Features

- **AI-Powered Recommendations** - LLM-based university matching and rationale generation
- **Client-Side CV Parsing** - Privacy-first PDF parsing in browser
- **Auth0 Integration** - Secure authentication with JWT tokens
- **Hybrid Architecture** - SQLite for transactional data, Parquet for university dataset
- **Personalized Weights** - Customizable recommendation factors
- **Feedback Loop** - Rate and refine recommendations

## 🏗️ Architecture

- **Backend**: Django 5 + Django REST Framework
- **Database**: SQLite (transactional), Parquet (dataset)
- **Query Engine**: DuckDB + Polars
- **Authentication**: Auth0 (JWT)
- **LLM Integration**: External API (OpenAI/Claude)
- **Frontend**: React + Vite (planned)

## 📊 API Endpoints

- `POST /api/auth/login/` - JWT authentication
- `GET/POST/PATCH /api/students/me/` - Student profile management
- `GET/PUT /api/students/preferences/` - Recommendation weights
- `POST /api/recommendations/run/` - **Generate recommendations** ⭐
- `GET /api/universities/` - Search universities
- `POST /api/feedback/recommendations/{id}/` - Submit feedback
- `GET /api/healthz/` - Health check

**Full API documentation**: [docs/apis/endpoints.md](docs/apis/endpoints.md)

## 🧪 Testing

```bash
# Run tests
cd backend
python manage.py test

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## 📦 Dataset Management

```bash
# Download dataset from Kaggle
python manage.py download_dataset --version 2025.09

# Load rankings (optional)
python manage.py load_webometrics --version 2025.09 --csv path/to/rankings.csv

# Curate and merge
python manage.py curate --version 2025.09

# Validate
python manage.py validate --version 2025.09

# Activate
python manage.py activate --version 2025.09
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Run `make lint` and `make test`
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.
