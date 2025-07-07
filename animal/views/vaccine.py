from core.viewsets.base import AutoPermissionViewSet
from django_filters.rest_framework import DjangoFilterBackend
from animal.models.vaccine import AnimalVaccine
from animal.serializers.vaccine import AnimalVaccineSerializer
from animal.filters.vaccine import AnimalVaccineFilter
from core.models.audit import UserLog
from core.constants.log_actions import LogActions

class AnimalVaccineViewSet(AutoPermissionViewSet):
    """
    Manage animal vaccine records
    Permissions:
    - animals.view
    - animals.manage
    """

    serializer_class = AnimalVaccineSerializer
    permission_module = "animals"
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnimalVaccineFilter

    def get_queryset(self):
        return AnimalVaccine.objects.filter(animal__farm=self.request.user.active_farm)

    def get_serializer_class(self):
        if self.action == "retrieve":
            from animal.serializers.vaccine import AnimalVaccineDetailSerializer
            return AnimalVaccineDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        vaccine = serializer.save(created_by=self.request.user)
        UserLog.objects.create(
            user=self.request.user,
            action=LogActions.VACCINE_ADDED,
            farm=self.request.user.active_farm,
        )
