from rest_framework import serializers
from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for student profiles."""
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'gpa', 'test_scores', 'interests', 'goals',
            'preferred_regions', 'country_preference', 
            'budget_min', 'budget_max', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_gpa(self, value):
        """Validate GPA is within acceptable range."""
        if value is not None and (value < 0.0 or value > 4.0):
            raise serializers.ValidationError("GPA must be between 0.0 and 4.0")
        return value
    
    def validate_budget_min(self, value):
        """Validate minimum budget is positive."""
        if value is not None and value < 0:
            raise serializers.ValidationError("Budget minimum must be positive")
        return value
    
    def validate_budget_max(self, value):
        """Validate maximum budget is positive."""
        if value is not None and value < 0:
            raise serializers.ValidationError("Budget maximum must be positive")
        return value
    
    def validate(self, data):
        """Validate budget range consistency."""
        budget_min = data.get('budget_min')
        budget_max = data.get('budget_max')
        
        if budget_min and budget_max and budget_min > budget_max:
            raise serializers.ValidationError(
                "Budget minimum cannot be greater than budget maximum"
            )
        
        return data
