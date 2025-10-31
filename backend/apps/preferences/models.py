from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Preference(models.Model):
    """User preferences for recommendation weights."""
    
    user = models.OneToOneField(
        User, 
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
