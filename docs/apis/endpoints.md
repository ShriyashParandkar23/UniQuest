# UniQuest API Endpoints Documentation

Complete reference for all UniQuest API endpoints.

**Base URL**: `http://localhost:8000` (development) | `https://api.uniquest.com` (production)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Student Profile](#student-profile)
3. [Preferences](#preferences)
4. [Recommendations](#recommendations)
5. [Feedback](#feedback)
6. [Universities](#universities)
7. [Dataset Management](#dataset-management)
8. [System](#system)
9. [API Documentation](#api-documentation)

---

## Authentication

### Login
Get JWT access and refresh tokens.

```http
POST /api/auth/login/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "alice@example.com",
  "password": "demo123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Errors:**
- `400 Bad Request` - Invalid credentials
- `401 Unauthorized` - Wrong email/password

---

### Refresh Token
Get a new access token using refresh token.

```http
POST /api/auth/refresh/
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### Verify Token
Check if a token is valid.

```http
POST /api/auth/verify/
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{}
```

**Errors:**
- `401 Unauthorized` - Token is invalid or expired

---

## Student Profile

### Get My Profile
Get the authenticated user's student profile.

```http
GET /api/students/me/
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user": 1,
  "gpa": 3.8,
  "test_scores": {
    "TOEFL": 110,
    "GRE_Q": 165,
    "GRE_V": 158,
    "GRE_AWA": 4.0
  },
  "interests": "Computer Science, AI, Machine Learning",
  "goals": "Pursue PhD in AI",
  "preferred_regions": ["US", "CA", "UK"],
  "country_preference": "US",
  "budget_min": 0,
  "budget_max": 50000,
  "created_at": "2025-10-28T10:00:00Z",
  "updated_at": "2025-10-28T10:00:00Z"
}
```

**Errors:**
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Profile doesn't exist

---

### Create Profile
Create a new student profile.

```http
POST /api/students/me/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "gpa": 3.8,
  "test_scores": {
    "TOEFL": 110,
    "GRE_Q": 165,
    "GRE_V": 158,
    "GRE_AWA": 4.0
  },
  "interests": "Computer Science, AI, Machine Learning",
  "goals": "Pursue PhD in AI and work on cutting-edge research",
  "preferred_regions": ["US", "CA", "UK"],
  "country_preference": "US",
  "budget_min": 0,
  "budget_max": 50000
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user": 1,
  "gpa": 3.8,
  ...
}
```

**Field Descriptions:**
- `gpa` (decimal, 0.0-4.0) - GPA on 4.0 scale
- `test_scores` (object) - Test scores (TOEFL, GRE, SAT, etc.)
- `interests` (string) - Academic and career interests
- `goals` (string) - Educational and career goals
- `preferred_regions` (array) - ISO 2-letter country codes
- `country_preference` (string) - Primary country preference
- `budget_min` (decimal) - Minimum budget in USD
- `budget_max` (decimal) - Maximum budget in USD

---

### Update Profile
Update specific fields in the profile.

```http
PATCH /api/students/me/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body (partial update):**
```json
{
  "gpa": 3.9,
  "test_scores": {
    "TOEFL": 115
  },
  "budget_max": 60000
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user": 1,
  "gpa": 3.9,
  ...
}
```

---

## Preferences

### Get Preferences
Get user's recommendation weights.

```http
GET /api/students/preferences/
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user": 1,
  "weights": {
    "academics": 0.30,
    "interests": 0.20,
    "career": 0.20,
    "location": 0.10,
    "budget": 0.10,
    "ranking": 0.05,
    "research_activity": 0.05
  },
  "created_at": "2025-10-28T10:00:00Z",
  "updated_at": "2025-10-28T10:00:00Z"
}
```

---

### Update Preferences
Update recommendation weights.

```http
PUT /api/students/preferences/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "weights": {
    "academics": 0.35,
    "interests": 0.25,
    "career": 0.20,
    "location": 0.10,
    "budget": 0.05,
    "ranking": 0.03,
    "research_activity": 0.02
  }
}
```

**Weight Factors:**
- `academics` (0.0-1.0) - Academic fit importance
- `interests` (0.0-1.0) - Interest alignment importance
- `career` (0.0-1.0) - Career preparation importance
- `location` (0.0-1.0) - Location preference importance
- `budget` (0.0-1.0) - Budget fit importance
- `ranking` (0.0-1.0) - University ranking importance
- `research_activity` (0.0-1.0) - Research output importance

**Note:** Weights should sum to 1.0 (100%)

**Response (200 OK):**
```json
{
  "id": 1,
  "user": 1,
  "weights": { ... },
  "updated_at": "2025-10-28T11:00:00Z"
}
```

---

## Recommendations

### Generate Recommendations ⭐
Generate personalized university recommendations using LLM.

**This is the main endpoint!**

```http
POST /api/recommendations/run/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "filters": {
    "countries": ["US", "CA", "UK"],
    "max_rank": 500,
    "budget_max": 50000
  },
  "weights": {
    "academics": 0.30,
    "interests": 0.20,
    "career": 0.20,
    "location": 0.15,
    "budget": 0.10,
    "ranking": 0.03,
    "research_activity": 0.02
  },
  "top_n": 20
}
```

**Filter Options:**
- `countries` (array) - ISO 2-letter country codes
- `max_rank` (integer) - Maximum Webometrics ranking
- `budget_max` (decimal) - Maximum budget in USD
- `search` (string) - Search term for university name

**Request Parameters:**
- `filters` (object) - Filters to apply to dataset
- `weights` (object, optional) - Custom weights (uses saved preferences if not provided)
- `top_n` (integer, optional) - Number of recommendations (default: 20)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user": 1,
    "university_ref": "I123456789",
    "display_name": "Stanford University",
    "country_code": "US",
    "score": 0.92,
    "rationale": "Stanford's world-class Computer Science program aligns perfectly with your AI research interests. With a GPA of 3.8 and strong GRE scores, you're a competitive candidate. The university's extensive research output (150,000+ publications) and Silicon Valley location offer unparalleled opportunities for ML research and industry connections.",
    "program": null,
    "filters": { ... },
    "weights": { ... },
    "generated_at": "2025-10-28T12:00:00Z"
  },
  // ... 19 more recommendations
]
```

**Processing Time:** 2-3 seconds (with parallel LLM calls)

**What Happens:**
1. Query dataset with filters (40 candidates)
2. Score each university using LLM (parallel)
3. Apply user weights to adjust scores
4. Sort by final score
5. Generate personalized rationales for top 20 (parallel)
6. Save recommendations to database
7. Return ranked list

---

### List My Recommendations
Get user's recommendation history.

```http
GET /api/recommendations/
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "university_ref": "I123456789",
    "display_name": "Stanford University",
    "score": 0.92,
    "rationale": "...",
    "generated_at": "2025-10-28T12:00:00Z"
  },
  // ... more recommendations
]
```

---

## Feedback

### Submit Feedback
Provide feedback for a specific recommendation.

```http
POST /api/feedback/recommendations/{recommendation_id}/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Path Parameters:**
- `recommendation_id` (integer) - ID of the recommendation

**Request Body:**
```json
{
  "rating": 5,
  "notes": "Perfect match! This university aligns perfectly with my research interests in AI."
}
```

**Field Descriptions:**
- `rating` (integer, 1-5) - Star rating
  - 1-2: Negative feedback
  - 3: Neutral
  - 4-5: Positive feedback
- `notes` (string, optional) - Detailed feedback

**Response (201 Created):**
```json
{
  "id": 1,
  "user": 1,
  "recommendation": 1,
  "rating": 5,
  "notes": "Perfect match!...",
  "created_at": "2025-10-28T13:00:00Z"
}
```

**Errors:**
- `404 Not Found` - Recommendation doesn't exist
- `400 Bad Request` - Duplicate feedback (one per recommendation)

---

### List My Feedback
Get all feedback submitted by the user.

```http
GET /api/feedback/
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "recommendation": {
      "id": 1,
      "university_ref": "I123456789",
      "display_name": "Stanford University",
      "score": 0.92
    },
    "rating": 5,
    "notes": "Perfect match!",
    "created_at": "2025-10-28T13:00:00Z"
  },
  // ... more feedback
]
```

---

## Universities

### Search Universities
Search universities in the dataset.

```http
GET /api/universities/?q=stanford&country=US&has_rank=true&limit=20&offset=0
```

**Query Parameters:**
- `q` (string, optional) - Search term (matches university name)
- `country` (string, optional) - ISO 2-letter country code
- `has_rank` (boolean, optional) - Filter universities with rankings
- `limit` (integer, optional) - Results per page (default: 20)
- `offset` (integer, optional) - Pagination offset (default: 0)
- `ordering` (string, optional) - Sort field: `display_name`, `country`, `rank`, `works_count`

**Response (200 OK):**
```json
{
  "count": 150,
  "next": "/api/universities/?offset=20",
  "previous": null,
  "results": [
    {
      "id": "I123456789",
      "display_name": "Stanford University",
      "canonical_name": "stanford-university",
      "country_code": "US",
      "homepage_url": "https://www.stanford.edu",
      "webometrics_rank": 2,
      "works_count": 150000,
      "cited_by_count": 5000000,
      "geo_latitude": 37.4275,
      "geo_longitude": -122.1697,
      "has_rank": true
    },
    // ... more universities
  ]
}
```

---

### Get University Details
Get detailed information about a specific university.

```http
GET /api/universities/{university_id}/
```

**Path Parameters:**
- `university_id` (string) - OpenAlex institution ID (e.g., "I123456789")

**Response (200 OK):**
```json
{
  "id": "I123456789",
  "display_name": "Stanford University",
  "canonical_name": "stanford-university",
  "country_code": "US",
  "homepage_url": "https://www.stanford.edu",
  "webometrics_rank": 2,
  "works_count": 150000,
  "cited_by_count": 5000000,
  "geo_latitude": 37.4275,
  "geo_longitude": -122.1697,
  "has_rank": true
}
```

**Errors:**
- `404 Not Found` - University doesn't exist in dataset

---

## Dataset Management

### List Ingestion Runs
Get history of dataset ingestion runs (admin).

```http
GET /api/ingestion/runs/
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "source": "openalex",
    "version": "2025.09",
    "status": "SUCCESS",
    "started_at": "2025-10-01T00:00:00Z",
    "finished_at": "2025-10-01T00:30:00Z",
    "stats": {
      "total_records": 25000,
      "countries": 180,
      "ranked_institutions": 5000
    },
    "error": ""
  },
  // ... more runs
]
```

**Status Values:**
- `PENDING` - Queued but not started
- `RUNNING` - Currently processing
- `SUCCESS` - Completed successfully
- `FAILED` - Failed with errors
- `CANCELLED` - Manually cancelled

---

## System

### Health Check
Check if the API is running and healthy.

```http
GET /api/healthz/
```

**No authentication required.**

**Response (200 OK):**
```json
{
  "status": "healthy",
  "database": "connected",
  "dataset": {
    "version": "2025.09",
    "institutions": 25000,
    "last_updated": "2025-10-01T00:00:00Z"
  },
  "timestamp": "2025-10-28T14:00:00Z"
}
```

---

## API Documentation

### OpenAPI Schema
Get the OpenAPI 3.0 schema in JSON format.

```http
GET /api/schema/
```

**Response (200 OK):**
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "UniQuest API",
    "version": "1.0.0"
  },
  "paths": { ... }
}
```

---

### Swagger UI
Interactive API documentation.

```http
GET /api/docs/
```

**Open in browser** for interactive testing interface.

---

### ReDoc
Alternative API documentation.

```http
GET /api/redoc/
```

**Open in browser** for clean, readable documentation.

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here",
  "code": "error_code"
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `authentication_failed` | 401 | Invalid or missing token |
| `not_found` | 404 | Resource not found |
| `validation_error` | 400 | Invalid request data |
| `permission_denied` | 403 | No permission to access |
| `server_error` | 500 | Internal server error |

---

## Rate Limiting

Currently no rate limiting is implemented. Future implementation will include:
- 100 requests per minute per user
- 10 recommendation generations per hour
- Burst allowance for testing

---

## Pagination

List endpoints support pagination:

```http
GET /api/universities/?limit=20&offset=40
```

**Response includes:**
```json
{
  "count": 150,
  "next": "/api/universities/?limit=20&offset=60",
  "previous": "/api/universities/?limit=20&offset=20",
  "results": [ ... ]
}
```

---

## Filtering & Sorting

### Filtering
Use query parameters:
```http
GET /api/universities/?country=US&has_rank=true
```

### Sorting
Use `ordering` parameter:
```http
GET /api/universities/?ordering=rank
GET /api/universities/?ordering=-works_count  # Descending
```

---

## Best Practices

1. **Always use HTTPS in production**
2. **Store tokens securely** - Never in localStorage
3. **Refresh tokens before expiry** - Use refresh endpoint
4. **Handle errors gracefully** - Check status codes
5. **Use pagination** - Don't fetch all results at once
6. **Cache responses** - Reduce API calls
7. **Validate inputs** - Check data before sending

---

## Examples

### Complete Workflow Example

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "demo123"}'

# Response: {"access": "...", "refresh": "..."}

# 2. Create Profile
curl -X POST http://localhost:8000/api/students/me/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"gpa": 3.8, "test_scores": {"TOEFL": 110}, ...}'

# 3. Generate Recommendations
curl -X POST http://localhost:8000/api/recommendations/run/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"filters": {"countries": ["US"]}, "top_n": 20}'

# 4. Submit Feedback
curl -X POST http://localhost:8000/api/feedback/recommendations/1/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "notes": "Perfect match!"}'
```

---

**Last Updated:** October 28, 2025  
**API Version:** 1.0  
**Base URL:** http://localhost:8000 (development)

