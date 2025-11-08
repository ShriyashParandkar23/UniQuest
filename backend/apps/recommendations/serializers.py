from rest_framework import serializers
from .models import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for recommendations."""
    
    score_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'university_ref', 'program', 'score', 'score_percentage',
            'rationale', 'filters', 'weights', 'generated_at'
        ]
        read_only_fields = ['id', 'generated_at']


class RecommendationRequestSerializer(serializers.Serializer):
    """Serializer for recommendation generation requests."""
    
    filters = serializers.JSONField(
        required=False,
        default=dict,
        help_text="Filters to apply when searching for universities"
    )
    
    weights = serializers.JSONField(
        required=False,
        default=dict,
        help_text="Weights for different recommendation factors"
    )
    
    top_n = serializers.IntegerField(
        default=20,
        min_value=1,
        max_value=100,
        help_text="Number of top recommendations to return (camelCase: topN in JSON)"
    )
    
    def validate_filters(self, value):
        """Validate filters structure."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Filters must be a dictionary")
        
        # Add specific filter validation here if needed
        return value
    
    def validate_weights(self, value):
        """Validate weights structure."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Weights must be a dictionary")
        
        valid_factors = {
            'academics', 'interests', 'career', 'location', 
            'budget', 'ranking', 'research_activity', 'researchActivity'
        }
        
        for factor, weight in value.items():
            if factor not in valid_factors:
                raise serializers.ValidationError(
                    f"Invalid weight factor: {factor}"
                )
            
            if not isinstance(weight, (int, float)):
                raise serializers.ValidationError(
                    f"Weight for {factor} must be a number"
                )
            
            if not (0.0 <= weight <= 1.0):
                raise serializers.ValidationError(
                    f"Weight for {factor} must be between 0.0 and 1.0"
                )
        
        return value
