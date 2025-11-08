# API Testing Guide

## ✅ Changes Completed

### 1. camelCase JSON API
- ✅ Added `djangorestframework-camel-case>=1.4.2` to requirements.txt
- ✅ Configured CamelCaseJSONRenderer and CamelCaseJSONParser in settings
- ✅ All API documentation updated to show camelCase examples
- ✅ Database schema diagram updated

### 2. Authentication Disabled
- ✅ Changed `DEFAULT_PERMISSION_CLASSES` to `AllowAny` in settings
- ✅ Updated all views to use `AllowAny` instead of `IsAuthenticated`
- ✅ Removed Authorization headers from documentation

## ⚠️ Known Issues

### Views That Reference `request.user`

These views will have issues when authentication is disabled because `request.user` will be `AnonymousUser`:

1. **`apps/students/views.py`** - Line 18
   - `StudentProfile.objects.get_or_create(user=self.request.user)`
   - **Issue**: AnonymousUser cannot be used as ForeignKey

2. **`apps/recommendations/views.py`** - Line 28, 95
   - `Recommendation.objects.filter(user=self.request.user)`
   - **Issue**: Will return empty queryset

3. **`apps/preferences/views.py`** - Line 16
   - `Preference.objects.get_or_create(user=self.request.user)`
   - **Issue**: AnonymousUser cannot be used as ForeignKey

4. **`apps/feedback/views.py`** - Lines 23, 28, 46, 74
   - Multiple references to `request.user`
   - **Issue**: Cannot create feedback for AnonymousUser

5. **`apps/users/views.py`** - Line 14
   - `user = request.user`
   - **Issue**: Will return AnonymousUser data

## 🧪 Testing Instructions

### Option 1: Manual Testing with curl

```bash
# 1. Start the server
cd backend
python manage.py runserver

# 2. Test health check (should work)
curl http://localhost:8000/api/healthz/

# 3. Test student profile (may fail due to AnonymousUser)
curl -X PATCH http://localhost:8000/api/students/me/ \
  -H "Content-Type: application/json" \
  -d '{
    "academicLevel": "bachelors",
    "gpa": 3.8,
    "testScores": [{"examName": "IELTS", "score": 7.5}]
  }'

# 4. Test search universities (should work)
curl "http://localhost:8000/api/universities/?q=stanford&limit=5"

# 5. Test preferences (may fail due to AnonymousUser)
curl -X PUT http://localhost:8000/api/students/preferences/ \
  -H "Content-Type: application/json" \
  -d '{"weights": {"academics": 0.3, "interests": 0.2}}'
```

### Option 2: Use Test Scripts

```bash
# Bash script
cd backend
chmod +x test_all_apis.sh
./test_all_apis.sh

# Python script
python test_apis.py
```

### Option 3: Use Postman/HTTP Client

Import the Postman collection from `docs/apis/UniQuest_API.postman_collection.json` and test endpoints.

## ✅ Endpoints That Should Work

These endpoints don't depend on `request.user`:

1. ✅ `GET /api/healthz/` - Health check
2. ✅ `GET /api/universities/?q=...` - Search universities
3. ✅ `GET /api/universities/{id}/` - Get university details
4. ✅ `GET /api/ingestion/runs/` - List ingestion runs
5. ✅ `GET /api/schema/` - API schema
6. ✅ `GET /api/docs/` - Swagger UI
7. ✅ `GET /api/redoc/` - ReDoc UI

## ⚠️ Endpoints That May Fail

These endpoints reference `request.user` and may fail:

1. ⚠️ `GET /api/students/me/` - Needs user
2. ⚠️ `PATCH /api/students/me/` - Needs user
3. ⚠️ `GET /api/students/preferences/` - Needs user
4. ⚠️ `PUT /api/students/preferences/` - Needs user
5. ⚠️ `GET /api/recommendations/` - Needs user
6. ⚠️ `POST /api/recommendations/run/` - Needs user
7. ⚠️ `GET /api/feedback/` - Needs user
8. ⚠️ `POST /api/feedback/recommendations/{id}/` - Needs user
9. ⚠️ `GET /api/users/profile/` - Needs user

## 🔧 Quick Fix Options

### Option 1: Handle AnonymousUser Gracefully

Modify views to check if user is authenticated:

```python
def get_object(self):
    if not self.request.user.is_authenticated:
        return Response({
            'error': 'User authentication required'
        }, status=401)
    # ... rest of code
```

### Option 2: Accept user_id as Parameter

Modify views to accept `user_id` in request:

```python
def get_object(self):
    user_id = self.request.data.get('userId') or self.request.query_params.get('userId')
    if not user_id:
        return Response({'error': 'userId required'}, status=400)
    user = get_object_or_404(User, id=user_id)
    # ... rest of code
```

### Option 3: Use Default Test User

Create a default user for testing:

```python
def get_object(self):
    if not self.request.user.is_authenticated:
        # Use default test user
        user, _ = User.objects.get_or_create(
            email='test@example.com',
            defaults={'username': 'testuser'}
        )
    else:
        user = self.request.user
    # ... rest of code
```

## 📊 Test Results Summary

Run the test scripts to see which endpoints work:

```bash
cd backend
python test_apis.py
```

Expected results:
- ✅ Health check: PASS
- ✅ University search: PASS
- ⚠️ User-dependent endpoints: May FAIL (due to AnonymousUser)

## 🎯 Next Steps

1. **Test the APIs** using the provided scripts
2. **Fix user-dependent views** to handle AnonymousUser or accept user_id
3. **Verify camelCase conversion** is working in responses
4. **Update frontend** to use camelCase field names

---

**Note**: The camelCase conversion is configured correctly. The main issue is views that need user context but authentication is disabled.

