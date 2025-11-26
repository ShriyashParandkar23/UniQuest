from rest_framework import serializers
from .models import College

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = [
            "id",
            "world_rank",
            "institution",
            "country",
            "national_rank",
            "quality_of_education",
            "alumni_employment",
            "quality_of_faculty",
            "publications",
            "influence",
            "citations",
            "broad_impact",
            "patents",
            "score",
            "year",
        ]
