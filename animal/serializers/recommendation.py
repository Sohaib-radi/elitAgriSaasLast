# animal/serializers/recommendation.py

from rest_framework import serializers
from animal.models.recommendation import VaccineRecommendation

class VaccineRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineRecommendation
        fields = [
            "id",
            "species",
            "vaccine_name",
            "description",
            "recommended_age_days",
            "repeat_interval_days",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]
