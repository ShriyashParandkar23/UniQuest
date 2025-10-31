from rest_framework import serializers
from .models import Preference


class PreferenceSerializer(serializers.ModelSerializer):
    """Serializer for user preferences."""
    
    class Meta:
        model = Preference
        fields = ['id', 'weights', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_weights(self, value):
        """Validate weights structure and values."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Weights must be a dictionary")
        
        valid_factors = {
            'academics', 'interests', 'career', 'location', 
            'budget', 'ranking', 'research_activity'
        }
        
        for factor, weight in value.items():
            if factor not in valid_factors:
                raise serializers.ValidationError(
                    f"Invalid weight factor: {factor}. "
                    f"Valid factors are: {', '.join(valid_factors)}"
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
    
    def create(self, validated_data):
        """Create preference with normalized weights."""
        preference = Preference(**validated_data)
        preference.normalize_weights()
        preference.save()
        return preference
    
    def update(self, instance, validated_data):
        """Update preference with normalized weights."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.normalize_weights()
        instance.save()
        return instance
