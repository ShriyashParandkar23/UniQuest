from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import json

User = get_user_model()


class StudentProfile(models.Model):
    """Student profile with academic and preference information."""
    
    ACADEMIC_LEVEL_CHOICES = [
        ('high-school', 'High School'),
        ('bachelors', "Bachelor's Degree"),
        ('masters', "Master's Degree"),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]
    
    CAMPUS_PREFERENCE_CHOICES = [
        ('Urban', 'Urban'),
        ('Suburban', 'Suburban'),
        ('Rural', 'Rural'),
        ('Any', 'Any'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    
    # Academic Information
    academic_level = models.CharField(
        max_length=20,
        choices=ACADEMIC_LEVEL_CHOICES,
        blank=True,
        null=True,
        help_text="Current or target academic level"
    )
    
    gpa = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        null=True, 
        blank=True,
        help_text="GPA on 4.0 scale"
    )
    
    academic_background = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of academic background entries with level, course, institution, year_of_completion, gpa"
    )
    
    work_experience = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of work experience entries"
    )
    
    test_scores = models.JSONField(
        default=list, 
        blank=True,
        help_text="Array of test scores with exam_name, score, test_date"
    )
    
    # Interests and Goals
    interests = models.TextField(
        blank=True,
        help_text="Academic and career interests"
    )
    
    preferred_programs = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of preferred academic programs/fields of study"
    )
    
    goals = models.TextField(
        blank=True,
        help_text="Educational and career goals"
    )
    
    # Location Preferences
    preferred_regions = models.JSONField(
        default=list, 
        blank=True,
        help_text="List of preferred regions/countries"
    )
    
    preferred_countries = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of preferred countries (full names or ISO codes)"
    )
    
    country_preference = models.CharField(
        max_length=2, 
        blank=True,
        help_text="ISO 2-letter country code for primary preference"
    )
    
    campus_preference = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of campus preferences (Urban, Suburban, Rural)"
    )
    
    # Budget Information
    budget_currency = models.CharField(
        max_length=3,
        default='USD',
        blank=True,
        help_text="ISO 3-letter currency code (e.g., USD, EUR, GBP)"
    )
    
    budget_min = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Minimum budget"
    )
    
    budget_max = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Maximum budget (maxTuition)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_profiles'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['country_preference']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Profile for {self.user.email}"
    
    @property
    def interests_list(self):
        """Return interests as a list if stored as JSON."""
        if isinstance(self.interests, str):
            try:
                return json.loads(self.interests)
            except json.JSONDecodeError:
                return [self.interests]
        return self.interests or []
    
    def get_test_score(self, test_name):
        """Get a specific test score from the array."""
        if not isinstance(self.test_scores, list):
            return None
        for test in self.test_scores:
            if isinstance(test, dict) and test.get('exam_name', '').upper() == test_name.upper():
                return test.get('score')
        return None
    
    def set_test_score(self, test_name, score, test_date=None):
        """Set or update a specific test score in the array."""
        if not isinstance(self.test_scores, list):
            self.test_scores = []
        
        # Check if test already exists
        for i, test in enumerate(self.test_scores):
            if isinstance(test, dict) and test.get('exam_name', '').upper() == test_name.upper():
                self.test_scores[i] = {
                    'exam_name': test_name,
                    'score': score,
                    'test_date': test_date or test.get('test_date', '')
                }
                return
        
        # Add new test score
        self.test_scores.append({
            'exam_name': test_name,
            'score': score,
            'test_date': test_date or ''
        })
