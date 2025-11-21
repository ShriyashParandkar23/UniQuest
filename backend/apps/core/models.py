"""
Consolidated models for UniQuest Core App.
All models from separate apps merged into single app.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import json


# ============================================================================
# USER MANAGEMENT
# ============================================================================

class User(AbstractUser):
    """Extended User model for UniQuest."""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# ============================================================================
# STUDENT PROFILE
# ============================================================================

class StudentProfile(models.Model):
    """Student profile with academic and preference information."""
    
    user = models.OneToOneField(
        'User',
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


# ============================================================================
# PREFERENCES
# ============================================================================

class Preference(models.Model):
    """User preferences for recommendation weights."""
    
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE, 
        related_name='preferences'
    )
    
    # Recommendation weights (0.0 to 1.0)
    weights = models.JSONField(
        default=dict,
        help_text="Weights for different recommendation factors"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'preferences'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['updated_at']),
        ]
    
    def __str__(self):
        return f"Preferences for {self.user.email}"
    
    def get_default_weights(self):
        """Return default weights for recommendations."""
        return {
            'academics': 0.3,
            'interests': 0.2,
            'career': 0.2,
            'location': 0.1,
            'budget': 0.1,
            'ranking': 0.05,
            'research_activity': 0.05
        }
    
    def get_weight(self, factor):
        """Get weight for a specific factor."""
        return self.weights.get(factor, self.get_default_weights().get(factor, 0.0))
    
    def set_weight(self, factor, weight):
        """Set weight for a specific factor."""
        if not self.weights:
            self.weights = self.get_default_weights()
        
        # Clamp weight to [0, 1] range
        weight = max(0.0, min(1.0, float(weight)))
        self.weights[factor] = weight
    
    def normalize_weights(self):
        """Normalize all weights to sum to 1.0."""
        if not self.weights:
            self.weights = self.get_default_weights()
            return
        
        total = sum(self.weights.values())
        if total > 0:
            for factor in self.weights:
                self.weights[factor] = self.weights[factor] / total
    
    def save(self, *args, **kwargs):
        """Override save to ensure weights are set."""
        if not self.weights:
            self.weights = self.get_default_weights()
        super().save(*args, **kwargs)


# ============================================================================
# RECOMMENDATIONS
# ============================================================================

class Recommendation(models.Model):
    """University recommendation for a user."""
    
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    
    # University reference (OpenAlex ID or canonical key)
    university_ref = models.CharField(
        max_length=255,
        help_text="OpenAlex ID or canonical identifier for the university"
    )
    
    # Program/degree information (optional)
    program = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Specific program or degree recommended"
    )
    
    # Recommendation score
    score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Recommendation score from 0.0 to 1.0"
    )
    
    # AI-generated rationale
    rationale = models.TextField(
        help_text="Explanation for why this university was recommended"
    )
    
    # Snapshot of filters used for this recommendation
    filters = models.JSONField(
        default=dict,
        help_text="Filters used when generating this recommendation"
    )
    
    # Snapshot of weights used for this recommendation
    weights = models.JSONField(
        default=dict,
        help_text="Weights used when generating this recommendation"
    )
    
    # Timestamps
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recommendations'
        indexes = [
            models.Index(fields=['user', '-generated_at']),
            models.Index(fields=['university_ref']),
            models.Index(fields=['-score']),
            models.Index(fields=['-generated_at']),
        ]
        ordering = ['-generated_at', '-score']
    
    def __str__(self):
        return f"Recommendation for {self.user.email}: {self.university_ref} (score: {self.score:.2f})"
    
    @property
    def score_percentage(self):
        """Return score as percentage."""
        return int(self.score * 100)
    
    def get_filter_value(self, filter_name):
        """Get a specific filter value."""
        return self.filters.get(filter_name)
    
    def get_weight_value(self, weight_name):
        """Get a specific weight value."""
        return self.weights.get(weight_name, 0.0)


# ============================================================================
# FEEDBACK
# ============================================================================

class Feedback(models.Model):
    """User feedback on recommendations."""
    
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    
    recommendation = models.ForeignKey(
        'Recommendation',
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Optional feedback notes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'feedback'
        unique_together = ['user', 'recommendation']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['recommendation']),
            models.Index(fields=['rating']),
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback by {self.user.email} for {self.recommendation.university_ref} ({self.rating}/5)"
    
    @property
    def is_positive(self):
        """Return True if feedback is positive (4-5 stars)."""
        return self.rating >= 4
    
    @property
    def is_negative(self):
        """Return True if feedback is negative (1-2 stars)."""
        return self.rating <= 2


# ============================================================================
# DATASET MANAGEMENT
# ============================================================================

class IngestionRun(models.Model):
    """Metadata for dataset ingestion runs."""
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    source = models.CharField(
        max_length=100,
        help_text="Data source name (e.g., 'openalex', 'webometrics')"
    )
    
    version = models.CharField(
        max_length=50,
        help_text="Version identifier (e.g., '2025.09')"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    
    stats = models.JSONField(
        default=dict,
        blank=True,
        help_text="Statistics about the ingestion run"
    )
    
    error = models.TextField(
        blank=True,
        help_text="Error message if the run failed"
    )
    
    class Meta:
        db_table = 'ingestion_runs'
        unique_together = ['source', 'version']
        indexes = [
            models.Index(fields=['source', 'version']),
            models.Index(fields=['status']),
            models.Index(fields=['-started_at']),
        ]
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.source} {self.version} ({self.status})"
    
    @property
    def duration_seconds(self):
        """Return duration in seconds if finished."""
        if self.finished_at and self.started_at:
            delta = self.finished_at - self.started_at
            return delta.total_seconds()
        return None
    
    @property
    def is_completed(self):
        """Return True if the run is completed (success or failed)."""
        return self.status in ['SUCCESS', 'FAILED', 'CANCELLED']
    
    def get_stat(self, stat_name, default=None):
        """Get a specific statistic."""
        return self.stats.get(stat_name, default)
    
    def set_stat(self, stat_name, value):
        """Set a specific statistic."""
        if not self.stats:
            self.stats = {}
        self.stats[stat_name] = value

