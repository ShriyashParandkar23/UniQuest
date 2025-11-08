from rest_framework import serializers
from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for student profiles."""
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'academic_level', 'gpa', 'academic_background', 'work_experience',
            'test_scores', 'interests', 'preferred_programs', 'goals',
            'preferred_regions', 'preferred_countries', 'country_preference',
            'campus_preference', 'budget_currency', 'budget_min', 'budget_max',
            'created_at', 'updated_at'
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
    
    def validate_test_scores(self, value):
        """Validate test_scores array structure."""
        if not isinstance(value, list):
            raise serializers.ValidationError("test_scores must be an array")
        
        for test in value:
            if not isinstance(test, dict):
                raise serializers.ValidationError("Each test score must be an object")
            if 'exam_name' not in test or 'score' not in test:
                raise serializers.ValidationError("Each test score must have exam_name and score")
        
        return value
    
    def validate_academic_background(self, value):
        """Validate academic_background array structure."""
        if not isinstance(value, list):
            raise serializers.ValidationError("academic_background must be an array")
        
        for entry in value:
            if not isinstance(entry, dict):
                raise serializers.ValidationError("Each academic background entry must be an object")
            required_fields = ['level', 'course', 'institution', 'year_of_completion']
            for field in required_fields:
                if field not in entry:
                    raise serializers.ValidationError(f"academic_background entry missing required field: {field}")
        
        return value
    
    def validate_preferred_programs(self, value):
        """Validate preferred_programs is an array."""
        if not isinstance(value, list):
            raise serializers.ValidationError("preferred_programs must be an array")
        return value
    
    def validate_preferred_countries(self, value):
        """Validate preferred_countries is an array."""
        if not isinstance(value, list):
            raise serializers.ValidationError("preferred_countries must be an array")
        return value
    
    def validate_campus_preference(self, value):
        """Validate campus_preference is an array."""
        if not isinstance(value, list):
            raise serializers.ValidationError("campus_preference must be an array")
        valid_options = ['Urban', 'Suburban', 'Rural', 'Any']
        for pref in value:
            if pref not in valid_options:
                raise serializers.ValidationError(
                    f"Invalid campus preference: {pref}. Must be one of: {', '.join(valid_options)}"
                )
        return value
    
    def validate_budget_currency(self, value):
        """Validate budget_currency is a valid ISO currency code."""
        if value and len(value) != 3:
            raise serializers.ValidationError("budget_currency must be a 3-letter ISO currency code")
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
