from rest_framework import serializers
from .models import Feedback
from ..recommendations.models import Recommendation


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for feedback."""
    
    is_positive = serializers.ReadOnlyField()
    is_negative = serializers.ReadOnlyField()
    
    class Meta:
        model = Feedback
        fields = [
            'id', 'recommendation', 'rating', 'notes', 
            'is_positive', 'is_negative', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_recommendation(self, value):
        """Validate that the recommendation belongs to the current user."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if value.user != request.user:
                raise serializers.ValidationError(
                    "You can only provide feedback on your own recommendations"
                )
        return value
    
    def validate_rating(self, value):
        """Validate rating is within acceptable range."""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class FeedbackCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating feedback."""
    
    class Meta:
        model = Feedback
        fields = ['rating', 'notes']
    
    def validate_rating(self, value):
        """Validate rating is within acceptable range."""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
