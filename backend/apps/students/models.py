from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import json

User = get_user_model()


class StudentProfile(models.Model):
    """Student profile with academic and preference information."""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    
    # Academic Information
    gpa = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        null=True, 
        blank=True,
        help_text="GPA on 4.0 scale"
    )
    
    test_scores = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Test scores like SAT, ACT, GRE, TOEFL, etc."
    )
    
    # Interests and Goals
    interests = models.TextField(
        blank=True,
        help_text="Academic and career interests"
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
    
    country_preference = models.CharField(
        max_length=2, 
        blank=True,
        help_text="ISO 2-letter country code for primary preference"
    )
    
    # Budget Information
    budget_min = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Minimum budget in USD"
    )
    
    budget_max = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Maximum budget in USD"
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
        """Get a specific test score."""
        return self.test_scores.get(test_name.upper())
    
    def set_test_score(self, test_name, score):
        """Set a specific test score."""
        if not self.test_scores:
            self.test_scores = {}
        self.test_scores[test_name.upper()] = score
