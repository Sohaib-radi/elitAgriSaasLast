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
        queryset = VaccineRecommendation.objects.all().order_by("species", "recommended_age_days")
        
        species = self.request.query_params.get("species")
        applies_to_purchased = self.request.query_params.get("applies_to_purchased")

        if species:
            queryset = queryset.filter(species=species)

        if applies_to_purchased is not None:
            # Converts "true"/"false" string to proper boolean
            applies_to_purchased = applies_to_purchased.lower() == "true"
            queryset = queryset.filter(applies_to_purchased=applies_to_purchased)

        return queryset
