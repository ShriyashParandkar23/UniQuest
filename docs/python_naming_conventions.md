# Python Naming Conventions Guide

## Official Python Convention (PEP 8)

**Python's official style guide (PEP 8) strongly recommends `snake_case` for variables, functions, and methods.**

### Why Python Uses snake_case (Not camelCase)

1. **Official Standard**: PEP 8 is Python's official style guide, widely adopted by the Python community
2. **Readability**: Python emphasizes readability (`import this` - "Readability counts")
3. **Consistency**: All Python standard library uses snake_case
4. **Tooling**: Linters (flake8, pylint), formatters (black), and IDEs expect snake_case
5. **Community Expectation**: Other Python developers expect snake_case

---

## Python Naming Conventions (PEP 8)

| Type | Convention | Example | Notes |
|------|------------|---------|-------|
| **Variables** | `snake_case` | `user_name`, `test_scores` | Lowercase with underscores |
| **Functions** | `snake_case` | `get_user_profile()`, `calculate_score()` | Lowercase with underscores |
| **Methods** | `snake_case` | `def get_test_score():` | Lowercase with underscores |
| **Classes** | `PascalCase` | `StudentProfile`, `User` | First letter of each word capitalized |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `DEFAULT_WEIGHTS` | All uppercase with underscores |
| **Private** | `_leading_underscore` | `_internal_method()` | Single underscore prefix |
| **Module** | `snake_case` | `student_models.py` | Lowercase with underscores |
| **Package** | `snake_case` | `apps/students/` | Lowercase, no underscores preferred |

---

## Comparison: Java vs Python

### Java Convention
```java
// Java uses camelCase
public class StudentProfile {
    private String firstName;
    private List<TestScore> testScores;
    
    public String getFirstName() {
        return firstName;
    }
}
```

### Python Convention (PEP 8)
```python
# Python uses snake_case
class StudentProfile:
    def __init__(self):
        self.first_name = ""
        self.test_scores = []
    
    def get_first_name(self):
        return self.first_name
```

---

## Why Follow Python Conventions?

### 1. **Tooling & Linters**
Your project already uses tools that enforce PEP 8:
- **Black** (formatter) - expects snake_case
- **Flake8** (linter) - will warn about camelCase
- **MyPy** (type checker) - works best with standard conventions

### 2. **Django Framework**
Django (which you're using) follows PEP 8:
- Model fields: `user_name`, `created_at`
- Methods: `get_absolute_url()`, `save()`
- All Django code uses snake_case

### 3. **Code Reviews & Collaboration**
- Other Python developers expect snake_case
- Code reviews will flag camelCase as non-standard
- Open source contributions require PEP 8 compliance

### 4. **Readability**
Python's philosophy: "Readability counts"
```python
# snake_case - easier to read
user_profile = get_user_profile()
test_scores = calculate_test_scores()

# camelCase - less Pythonic
userProfile = getUserProfile()
testScores = calculateTestScores()
```

---

## Can You Use camelCase in Python?

**Technically yes, but strongly discouraged:**

### Problems with camelCase in Python:

1. **Linter Warnings**: Flake8 will flag it
   ```bash
   # Flake8 output
   E501: line too long
   W503: camelCase variable name (non-PEP 8)
   ```

2. **Inconsistent with Standard Library**
   ```python
   # Python standard library uses snake_case
   import os
   os.path.join()  # snake_case
   os.getcwd()     # snake_case
   
   # Your code would be inconsistent
   userProfile = getUserProfile()  # camelCase - stands out as wrong
   ```

3. **Django ORM Issues**
   ```python
   # Django expects snake_case
   StudentProfile.objects.filter(user_name="John")  # Works
   StudentProfile.objects.filter(userName="John")    # Error!
   ```

4. **Team/Community Pushback**
   - Code reviews will request changes
   - Open source contributions will be rejected
   - New team members will be confused

---

## Recommendation for Your Project

### ✅ **Use snake_case** (Recommended)

**Reasons:**
1. Your project already uses snake_case everywhere
2. Django framework uses snake_case
3. Your linters (flake8, black) expect snake_case
4. Python community standard
5. Better for long-term maintenance

**Current state:**
- ✅ Database columns: `snake_case` (user_name, test_scores)
- ✅ Python variables: `snake_case` (user_name, test_scores)
- ✅ Python methods: `snake_case` (get_test_score())
- ✅ JSON fields: `snake_case` (exam_name, test_date)
- ✅ Classes: `PascalCase` (StudentProfile, User)

### ❌ **Don't use camelCase** (Not Recommended)

**Why not:**
- Goes against PEP 8
- Inconsistent with Django
- Will trigger linter warnings
- Confuses other Python developers
- Makes code reviews harder

---

## Transitioning from Java to Python

### Mental Mapping:

| Java | Python |
|------|--------|
| `camelCase` variables | `snake_case` variables |
| `camelCase()` methods | `snake_case()` methods |
| `PascalCase` classes | `PascalCase` classes (same!) |
| `UPPER_CASE` constants | `UPPER_SNAKE_CASE` constants (same!) |

### Quick Reference:

```python
# ✅ Python way
class StudentProfile:                    # PascalCase for classes
    MAX_SCORE = 100                      # UPPER_SNAKE_CASE for constants
    
    def __init__(self):
        self.first_name = ""             # snake_case for attributes
        self.test_scores = []            # snake_case for attributes
    
    def get_test_score(self):            # snake_case for methods
        return self.test_scores[0]
    
    def _internal_helper(self):          # _leading_underscore for private
        pass

# ❌ Java way (don't do this in Python)
class StudentProfile:
    MAX_SCORE = 100
    
    def __init__(self):
        self.firstName = ""              # camelCase - wrong!
        self.testScores = []             # camelCase - wrong!
    
    def getTestScore(self):              # camelCase - wrong!
        return self.testScores[0]
```

---

## Your Current Codebase

Your project is **already correctly using snake_case**:

```python
# ✅ Current code (correct)
class StudentProfile(models.Model):
    academic_level = models.CharField(...)      # snake_case
    test_scores = models.JSONField(...)          # snake_case
    
    def get_test_score(self, test_name):       # snake_case method
        ...
```

This is the **correct Python way** and aligns with:
- ✅ PEP 8 standard
- ✅ Django conventions
- ✅ Your linter configuration
- ✅ Python community expectations

---

## Final Recommendation

**Stick with snake_case** - it's the Python standard and your codebase is already correctly using it. While camelCase feels natural coming from Java, Python's ecosystem (Django, linters, standard library) all use snake_case, so following the convention will make your code:
- More maintainable
- Easier for other Python developers to understand
- Compatible with Python tooling
- Consistent with Django framework

**The good news**: Classes still use `PascalCase` in Python (just like Java!), so that part feels familiar! 🎉

---

## Resources

- **PEP 8**: https://pep8.org/ (Official Python style guide)
- **Django Style Guide**: https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/
- **Google Python Style Guide**: https://google.github.io/styleguide/pyguide.html

---

**Bottom Line**: Python uses `snake_case` for variables/functions/methods, `PascalCase` for classes. This is the standard, and your codebase is already following it correctly! 👍

