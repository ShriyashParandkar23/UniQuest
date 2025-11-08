# Naming Conventions by Layer: Database, Models, and API

## Overview: Three Layers, Different Considerations

Your application has three distinct layers with different naming convention considerations:

1. **Database Layer** (SQLite columns)
2. **Model Layer** (Django model attributes)
3. **API Layer** (JSON request/response bodies)

---

## Current State Analysis

### ✅ Current Implementation (All snake_case)

**Database Columns:**
```sql
-- SQLite table
CREATE TABLE student_profiles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    academic_level VARCHAR(20),
    test_scores JSON,
    created_at DATETIME
);
```

**Model Attributes:**
```python
# Django model
class StudentProfile(models.Model):
    academic_level = models.CharField(...)
    test_scores = models.JSONField(...)
    created_at = models.DateTimeField(...)
```

**JSON API:**
```json
{
  "academic_level": "bachelors",
  "test_scores": [
    {
      "exam_name": "IELTS",
      "score": 7.5,
      "test_date": "2024-06"
    }
  ]
}
```

---

## Recommended Approach: Two Options

### Option 1: snake_case Everywhere (Current - Recommended for Python)

**Pros:**
- ✅ Consistent across all layers
- ✅ No transformation needed
- ✅ Simpler codebase
- ✅ Python/Django standard
- ✅ Works well with TypeScript (can use snake_case)

**Cons:**
- ❌ Frontend developers might prefer camelCase
- ❌ Less common in JavaScript ecosystem

**Implementation:**
```python
# No transformation needed - direct mapping
class StudentProfileSerializer(serializers.ModelSerializer):
    # Model field → JSON field (same name)
    academic_level = serializers.CharField()
    test_scores = serializers.JSONField()
```

---

### Option 2: snake_case Backend, camelCase API (Hybrid)

**Pros:**
- ✅ Frontend-friendly (JavaScript convention)
- ✅ Backend stays Pythonic
- ✅ Common in modern APIs

**Cons:**
- ❌ Requires transformation layer
- ❌ More complex serializers
- ❌ Potential for bugs in mapping

**Implementation:**
```python
# Requires field mapping
class StudentProfileSerializer(serializers.ModelSerializer):
    academicLevel = serializers.CharField(source='academic_level')
    testScores = serializers.JSONField(source='test_scores')
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'academicLevel', 'testScores']
```

---

## Detailed Recommendations by Layer

### 1. Database Columns (SQLite)

**✅ Use: `snake_case`**

**Why:**
- SQLite convention (case-insensitive but snake_case is standard)
- Django ORM uses snake_case by default
- SQL standard practice
- Easier to read in SQL queries

**Example:**
```sql
-- ✅ Good
CREATE TABLE student_profiles (
    user_id INTEGER,
    academic_level VARCHAR(20),
    test_scores JSON,
    created_at DATETIME
);

-- ❌ Bad (don't do this)
CREATE TABLE student_profiles (
    userId INTEGER,
    academicLevel VARCHAR(20),
    testScores JSON,
    createdAt DATETIME
);
```

**Django Model:**
```python
class StudentProfile(models.Model):
    # Django automatically converts to snake_case in DB
    academic_level = models.CharField(...)  # → academic_level in DB
    test_scores = models.JSONField(...)       # → test_scores in DB
    
    class Meta:
        db_table = 'student_profiles'  # snake_case table name
```

---

### 2. Model Attributes (Django Models)

**✅ Use: `snake_case`**

**Why:**
- Python PEP 8 standard
- Django convention
- Matches database columns
- No transformation needed

**Example:**
```python
# ✅ Good
class StudentProfile(models.Model):
    academic_level = models.CharField(max_length=20)
    test_scores = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_test_score(self, test_name):
        # Method also uses snake_case
        pass

# ❌ Bad (don't do this)
class StudentProfile(models.Model):
    academicLevel = models.CharField(...)  # Non-Pythonic
    testScores = models.JSONField(...)      # Non-Pythonic
```

---

### 3. JSON API Request/Response Bodies

**Decision Point: Choose One Approach**

#### Approach A: snake_case in JSON (Current - Recommended)

**When to use:**
- Frontend team is comfortable with snake_case
- Using TypeScript (supports both conventions)
- Want simplicity (no transformation)
- Python-first team

**Example:**
```json
// Request
POST /api/students/me/
{
  "academic_level": "bachelors",
  "test_scores": [
    {
      "exam_name": "IELTS",
      "score": 7.5,
      "test_date": "2024-06"
    }
  ]
}

// Response
{
  "id": 1,
  "academic_level": "bachelors",
  "test_scores": [...],
  "created_at": "2025-10-28T10:00:00Z"
}
```

**Serializer (No transformation):**
```python
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'academic_level', 'test_scores', 'created_at']
        # Direct mapping - no source needed
```

**Frontend (TypeScript/JavaScript):**
```typescript
// TypeScript interface
interface StudentProfile {
  academic_level: string;
  test_scores: TestScore[];
  created_at: string;
}

// Usage
const profile: StudentProfile = {
  academic_level: "bachelors",
  test_scores: [...]
};
```

---

#### Approach B: camelCase in JSON (Alternative)

**When to use:**
- Frontend team strongly prefers camelCase
- JavaScript/React team expects camelCase
- Want to match JavaScript conventions
- API is consumed by external clients expecting camelCase

**Example:**
```json
// Request
POST /api/students/me/
{
  "academicLevel": "bachelors",
  "testScores": [
    {
      "examName": "IELTS",
      "score": 7.5,
      "testDate": "2024-06"
    }
  ]
}

// Response
{
  "id": 1,
  "academicLevel": "bachelors",
  "testScores": [...],
  "createdAt": "2025-10-28T10:00:00Z"
}
```

**Serializer (With transformation):**
```python
class StudentProfileSerializer(serializers.ModelSerializer):
    # Map camelCase JSON → snake_case model
    academicLevel = serializers.CharField(source='academic_level')
    testScores = serializers.JSONField(source='test_scores')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'academicLevel', 'testScores', 'createdAt']
```

**Or use a custom field name mapping:**
```python
from rest_framework import serializers

class CamelCaseJSONRenderer(JSONRenderer):
    """Convert snake_case to camelCase in JSON responses."""
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Transform data keys from snake_case to camelCase
        return super().render(
            self._to_camel_case(data),
            accepted_media_type,
            renderer_context
        )
    
    def _to_camel_case(self, data):
        # Recursive conversion logic
        ...
```

**Frontend (TypeScript/JavaScript):**
```typescript
// TypeScript interface (matches JSON)
interface StudentProfile {
  academicLevel: string;
  testScores: TestScore[];
  createdAt: string;
}

// Usage (natural JavaScript style)
const profile: StudentProfile = {
  academicLevel: "bachelors",
  testScores: [...]
};
```

---

## Comparison Table

| Layer | snake_case (Current) | camelCase (Alternative) |
|-------|---------------------|--------------------------|
| **Database** | ✅ `academic_level` | ❌ Not recommended |
| **Model** | ✅ `academic_level` | ❌ Not recommended |
| **JSON API** | ✅ `academic_level` | ✅ `academicLevel` |
| **Frontend** | ✅ Works fine | ✅ More natural |

---

## Recommendation for Your Project

### ✅ **Stick with snake_case everywhere** (Current approach)

**Reasons:**
1. **Simplicity**: No transformation layer needed
2. **Consistency**: Same naming across all layers
3. **Python Standard**: Aligns with Python/Django conventions
4. **TypeScript Support**: TypeScript handles snake_case well
5. **Less Code**: No serializer mapping required
6. **Fewer Bugs**: No risk of mapping errors

**Your current implementation is correct:**
```python
# Model (snake_case)
academic_level = models.CharField(...)

# Serializer (snake_case - direct mapping)
class StudentProfileSerializer(serializers.ModelSerializer):
    # No source= needed - direct mapping
    academic_level = serializers.CharField()

# JSON (snake_case - matches model)
{
  "academic_level": "bachelors"
}
```

---

## If You Want camelCase in JSON

If your frontend team strongly prefers camelCase, here's how to implement it:

### Step 1: Install djangorestframework-camel-case (Recommended)

```bash
pip install djangorestframework-camel-case
```

### Step 2: Update Settings

```python
# settings/base.py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ],
}
```

### Step 3: Keep Models as snake_case

```python
# Models stay snake_case (Python convention)
class StudentProfile(models.Model):
    academic_level = models.CharField(...)  # snake_case
    test_scores = models.JSONField(...)     # snake_case
```

### Step 4: JSON Automatically Converts

```json
// Request (camelCase)
{
  "academicLevel": "bachelors",
  "testScores": [...]
}

// Automatically converted to snake_case for model
// academicLevel → academic_level
// testScores → test_scores

// Response (camelCase)
{
  "academicLevel": "bachelors",
  "testScores": [...]
}
```

**This way:**
- ✅ Database: snake_case
- ✅ Models: snake_case (Python standard)
- ✅ JSON: camelCase (JavaScript-friendly)
- ✅ Automatic conversion (no manual mapping)

---

## Summary

| Layer | Convention | Reason |
|-------|-----------|--------|
| **Database Columns** | `snake_case` | SQLite/Django standard |
| **Model Attributes** | `snake_case` | Python PEP 8 standard |
| **JSON API** | `snake_case` OR `camelCase` | Your choice (both work) |

**Current State: ✅ All snake_case** - This is correct and recommended!

**If frontend wants camelCase:** Use `djangorestframework-camel-case` package for automatic conversion while keeping backend in snake_case.

---

## Quick Decision Guide

**Use snake_case everywhere if:**
- ✅ You want simplicity
- ✅ Frontend team is flexible
- ✅ Python-first project
- ✅ TypeScript frontend (handles both)

**Use camelCase in JSON if:**
- ✅ Frontend team strongly prefers it
- ✅ External API consumers expect camelCase
- ✅ Willing to add transformation layer
- ✅ Use `djangorestframework-camel-case` package

**Your current approach (all snake_case) is perfectly valid and recommended!** 🎉

