from core.models.person import Person
from core.serializers.person import PersonSerializer
from core.viewsets.base import AutoPermissionViewSet



class PersonViewSet(AutoPermissionViewSet):
    """
    🧍 Manage People (external clients, suppliers, staff, etc.)
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_module = "people" 

    def get_queryset(self):
        return self.queryset.filter(farm=self.request.user.active_farm)
