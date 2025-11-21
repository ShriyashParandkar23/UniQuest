from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from ..recommendations.models import Recommendation

User = get_user_model()


class Feedback(models.Model):
    """User feedback on recommendations."""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    
    recommendation = models.ForeignKey(
        Recommendation,
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
