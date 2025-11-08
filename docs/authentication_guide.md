# Authentication Control in Django REST Framework

## Disabling Authentication at Controller/View Level

**Yes, it is possible to disable authentication at the REST controller/view level in Django REST Framework.**

### Method 1: Using `@permission_classes` Decorator

For function-based views:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])  # Disables authentication requirement
def public_endpoint(request):
    return Response({"message": "This endpoint is public"})
```

### Method 2: Using `permission_classes` Class Attribute

For class-based views:

```python
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class PublicAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]  # Disables authentication requirement
    
    def get(self, request, *args, **kwargs):
        return Response({"message": "This endpoint is public"})
```

### Method 3: Overriding `get_permissions()` Method

For more complex scenarios:

```python
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

class ConditionalAuthView(generics.RetrieveAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET is public
        return [IsAuthenticated()]  # POST/PUT/DELETE require auth
```

### Available Permission Classes

- **`AllowAny`** - No authentication required (public endpoint)
- **`IsAuthenticated`** - Requires valid authentication token
- **`IsAdminUser`** - Requires admin user
- **`IsAuthenticatedOrReadOnly`** - Auth required for write, read-only for GET
- **`DjangoModelPermissions`** - Django model-level permissions
- **`DjangoObjectPermissions`** - Object-level permissions

### Current Usage in UniQuest

Looking at the codebase, authentication is currently controlled at the view level:

**Example from `backend/apps/dataset/views.py`:**
```python
@api_view(['GET'])
@permission_classes([AllowAny])  # Health check is public
def health_check(request):
    return Response({"status": "healthy"})
```

**Example from `backend/apps/students/views.py`:**
```python
class StudentProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]  # Requires authentication
    # ...
```

### Global vs View-Level Settings

**Global Setting** (in `settings.py`):
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Default for all views
    ],
}
```

**View-Level Override** (takes precedence):
```python
class MyView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]  # Overrides global setting
```

### Best Practices

1. **Explicit is better than implicit** - Always specify `permission_classes` even if using global defaults
2. **Use `AllowAny` for public endpoints** - Health checks, public data, etc.
3. **Use `IsAuthenticated` for protected endpoints** - User data, recommendations, etc.
4. **Document authentication requirements** - In API documentation and code comments

### Example: Mixed Authentication

```python
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

class UniversityListView(generics.ListAPIView):
    permission_classes = [AllowAny]  # Public: anyone can search universities
    
class RecommendationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]  # Protected: requires login
```

---

**Note:** The `@permission_classes` decorator and `permission_classes` class attribute are the Django REST Framework equivalents of "annotations" in other frameworks (like Spring's `@PreAuthorize` in Java).

