# animal/views/recommendation.py

from core.viewsets.base import AutoPermissionViewSet
from animal.models.recommendation import VaccineRecommendation
from animal.serializers.recommendation import VaccineRecommendationSerializer


class VaccineRecommendationViewSet(AutoPermissionViewSet):
    """
    💉 Manage vaccine recommendations for newborn animals.
    Centralized permission: animals.view / animals.manage
    """
    serializer_class = VaccineRecommendationSerializer
    permission_module = "animals"

    def get_queryset(self):
        return VaccineRecommendation.objects.all().order_by("species", "recommended_age_days")
