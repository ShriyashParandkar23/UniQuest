# UniQuest API Documentation

Welcome to the UniQuest API documentation! This folder contains everything you need to test and integrate with the UniQuest API.

## 📁 Contents

- **`UniQuest_API.postman_collection.json`** - Complete Postman collection with all API endpoints
- **`UniQuest_Development.postman_environment.json`** - Development environment (localhost:8000)
- **`UniQuest_Production.postman_environment.json`** - Production environment template
- **`endpoints.md`** - Detailed API endpoint documentation

---

## 🚀 Quick Start with Postman

### Step 1: Import Collection
1. Open Postman
2. Click **Import** button (top left)
3. Drag and drop `UniQuest_API.postman_collection.json`
4. Click **Import**

### Step 2: Import Environment
1. Click **Import** again
2. Drag and drop `UniQuest_Development.postman_environment.json`
3. Click **Import**

### Step 3: Select Environment & Test
1. Click the environment dropdown (top right)
2. Select **"UniQuest Development"**
3. Navigate to **Authentication → Login**
4. Click **Send**
5. ✅ Tokens are automatically saved!

---

## 🔑 Authentication Flow

### 1. Login First
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "alice@example.com",
  "password": "demo123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Use Access Token
All authenticated endpoints require the access token:
```http
GET /api/students/me/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 📋 API Overview

### Authentication
- `POST /api/auth/login/` - Login with email/password
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/verify/` - Verify token validity

### Student Profile
- `GET /api/students/me/` - Get current user's profile
- `POST /api/students/me/` - Create profile
- `PATCH /api/students/me/` - Update profile

### Preferences
- `GET /api/students/preferences/` - Get recommendation weights
- `PUT /api/students/preferences/` - Update weights

### Recommendations ⭐
- `POST /api/recommendations/run/` - **Generate recommendations** (main endpoint!)
- `GET /api/recommendations/` - List recommendation history

### Feedback
- `POST /api/feedback/recommendations/{id}/` - Submit feedback
- `GET /api/feedback/` - List feedback history

### Universities
- `GET /api/universities/` - Search universities
- `GET /api/universities/{id}/` - Get university details

### System
- `GET /api/healthz/` - Health check (no auth required)

---

## 🎯 Common Workflows

### First-Time User Flow
```
1. POST /api/auth/login/              # Get tokens
2. POST /api/students/me/             # Create profile
3. PUT /api/students/preferences/     # Set weights
4. POST /api/recommendations/run/     # Generate recommendations
5. POST /api/feedback/recommendations/1/  # Provide feedback
```

### Returning User Flow
```
1. POST /api/auth/login/              # Get tokens
2. GET /api/students/me/              # Get profile
3. POST /api/recommendations/run/     # Generate new recommendations
4. GET /api/recommendations/          # View history
```

### Refinement Loop
```
1. PUT /api/students/preferences/     # Adjust weights
2. POST /api/recommendations/run/     # Regenerate
3. Compare results
4. Repeat until satisfied
```

---

## 💡 Key Features

### Auto-Save Tokens
The Login request in Postman automatically saves tokens to environment variables:
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
}
```

### Pre-filled Examples
Every request includes example data:
- Student profiles with realistic GPAs and test scores
- Recommendation filters with common countries
- Feedback with sample ratings and notes

### Smart Authorization
All authenticated endpoints automatically use `{{access_token}}` variable.

---

## 🔧 Environment Variables

### Development
```
base_url: http://localhost:8000
access_token: (auto-set after login)
refresh_token: (auto-set after login)
user_email: alice@example.com
user_password: demo123
```

### Production
```
base_url: https://api.uniquest.com
access_token: (set after login)
refresh_token: (set after login)
user_email: (your email)
user_password: (your password)
```

---

## 📝 Demo Credentials

For testing in development:
- **Email**: `alice@example.com`, `bob@example.com`, `carol@example.com`
- **Password**: `demo123` (for all demo users)

---

## 🐛 Troubleshooting

### "401 Unauthorized"
- **Cause**: Token expired or missing
- **Fix**: Run Login request again

### "404 Not Found"
- **Cause**: Server not running or wrong URL
- **Fix**: Start server with `python manage.py runserver`

### "500 Internal Server Error"
- **Cause**: Server-side error
- **Fix**: Check Django logs for details

### No Response
- **Cause**: Server not running
- **Fix**: Ensure Django server is running on port 8000

---

## 📚 Additional Resources

- **Interactive Docs**: http://localhost:8000/api/docs/ (Swagger UI)
- **Alternative Docs**: http://localhost:8000/api/redoc/ (ReDoc)
- **OpenAPI Schema**: http://localhost:8000/api/schema/
- **Backend README**: `../../backend/README.md`
- **User Journey**: `../user_journey.md`
- **Diagrams**: `../diagrams/`

---

## 🎨 Collection Structure

```
UniQuest API/
├── Authentication/
│   ├── Login
│   ├── Refresh Token
│   └── Verify Token
├── Student Profile/
│   ├── Get My Profile
│   ├── Create Profile
│   └── Update Profile
├── Preferences/
│   ├── Get Preferences
│   └── Update Preferences
├── Recommendations/
│   ├── Generate Recommendations ⭐
│   └── List My Recommendations
├── Feedback/
│   ├── Submit Feedback
│   └── List My Feedback
├── Universities/
│   ├── Search Universities
│   └── Get University Details
├── Dataset Management/
│   └── List Ingestion Runs
├── System/
│   └── Health Check
└── API Documentation/
    ├── OpenAPI Schema
    ├── Swagger UI
    └── ReDoc
```

---

## 🚦 API Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | No permission to access |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

---

## 📊 Rate Limiting

Currently no rate limiting is implemented. In production, consider:
- 100 requests per minute per user
- 10 recommendation generations per hour
- Burst allowance for testing

---

## 🔐 Security Best Practices

1. **Never commit tokens** - Use environment variables
2. **Rotate tokens regularly** - Use refresh endpoint
3. **Use HTTPS in production** - Encrypt all traffic
4. **Validate all inputs** - Server validates all data
5. **Monitor for abuse** - Track API usage

---

## 📈 Performance Tips

### Recommendation Generation
- **Expected time**: 2-3 seconds
- **Parallel processing**: LLM calls run in parallel
- **Caching**: Results cached for 1 hour
- **Optimization**: Reduce `top_n` for faster results

### Search Universities
- **Expected time**: 100-300ms
- **Pagination**: Use `limit` and `offset`
- **Filtering**: Use specific filters to reduce results

---

## 🆘 Need Help?

1. Check the **endpoints.md** file for detailed API documentation
2. Review **Postman Console** for detailed error messages
3. Check **Django server logs** for backend errors
4. Visit **http://localhost:8000/api/docs/** for interactive testing
5. Refer to **backend/README.md** for setup instructions

---

## 📞 Support

For questions or issues:
- Check the main project documentation
- Review the API documentation at `/api/docs/`
- Consult the user journey document
- Examine the sequence diagrams in `/docs/diagrams/`

---

**Happy Testing! 🚀**

Last Updated: October 28, 2025

