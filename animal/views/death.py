from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from core.viewsets.base import AutoPermissionViewSet
from animal.models.death import AnimalDeath
from animal.serializers.death import AnimalDeathSerializer
from animal.filters.death import AnimalDeathFilter
from core.constants.log_actions import LogActions
from core.models.audit import UserLog

class AnimalDeathViewSet(AutoPermissionViewSet):
    serializer_class = AnimalDeathSerializer
    permission_module = "animal_deaths"
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnimalDeathFilter

    def get_queryset(self):
        return AnimalDeath.objects.filter(animal__farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        animal = serializer.validated_data["animal"]

        # 1. Soft-delete the animal (mark as inactive)
        animal.is_active = False
        animal.save()

        # 2. Log the death action
        UserLog.objects.create(
            user=self.request.user,
            action=LogActions.ANIMAL_DEATH,
            farm=animal.farm,
            description=f"Marked animal {animal.animal_number} as deceased."
        )

        # 3. Save the death record
        serializer.save(
            farm=animal.farm,
            created_by=self.request.user
        )
