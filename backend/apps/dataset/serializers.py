from rest_framework import serializers
from .models import IngestionRun


class IngestionRunSerializer(serializers.ModelSerializer):
    """Serializer for ingestion runs."""
    
    duration_seconds = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    
    class Meta:
        model = IngestionRun
        fields = [
            'id', 'source', 'version', 'status', 'started_at', 'finished_at',
            'stats', 'error', 'duration_seconds', 'is_completed'
        ]
        read_only_fields = ['id', 'started_at', 'finished_at']


class UniversitySearchSerializer(serializers.Serializer):
    """Serializer for university search parameters."""
    
    q = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Search query for university name"
    )
    
    country = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=2,
        help_text="2-letter country code"
    )
    
    has_rank = serializers.BooleanField(
        required=False,
        help_text="Filter universities with webometrics ranking"
    )
    
    limit = serializers.IntegerField(
        default=20,
        min_value=1,
        max_value=100,
        help_text="Maximum number of results"
    )
    
    offset = serializers.IntegerField(
        default=0,
        min_value=0,
        help_text="Offset for pagination"
    )
    
    ordering = serializers.ChoiceField(
        choices=['display_name', 'country', 'rank', 'works_count'],
        default='display_name',
        help_text="Field to order by"
    )


class UniversitySerializer(serializers.Serializer):
    """Serializer for university data."""
    
    id = serializers.CharField()
    display_name = serializers.CharField()
    canonical_name = serializers.CharField(allow_null=True)
    country_code = serializers.CharField(allow_null=True)
    homepage_url = serializers.URLField(allow_null=True)
    webometrics_rank = serializers.IntegerField(allow_null=True)
    works_count = serializers.IntegerField(allow_null=True)
    cited_by_count = serializers.IntegerField(allow_null=True)
    geo_latitude = serializers.FloatField(allow_null=True)
    geo_longitude = serializers.FloatField(allow_null=True)
    has_rank = serializers.BooleanField()


class DatasetValidationSerializer(serializers.Serializer):
    """Serializer for dataset validation results."""
    
    valid = serializers.BooleanField()
    version = serializers.CharField(allow_null=True)
    dataset_path = serializers.CharField(allow_null=True)
    error = serializers.CharField(allow_null=True)
    stats = serializers.JSONField()
