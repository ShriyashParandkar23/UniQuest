from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Recommendation(models.Model):
    """University recommendation for a user."""
    
    user = models.ForeignKey(
        User,
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
