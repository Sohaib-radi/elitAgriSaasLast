from core.viewsets.base import AutoPermissionViewSet
from animal.models.animal import Animal
from animal.serializers.animal import AnimalSerializer
from animal.filters.animal import AnimalFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response

class AnimalViewSet(AutoPermissionViewSet):
    serializer_class = AnimalSerializer
    permission_module = "animals"  
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnimalFilter

    def get_queryset(self):
        return Animal.objects.filter(
            farm=self.request.user.active_farm,
            is_active=True
        )

    def create(self, request, *args, **kwargs):
        data = request.data
        many = isinstance(data, list)

        if many:
            for item in data:
                item["farm"] = request.user.active_farm.id
                item["created_by"] = request.user.id
        else:
            data["farm"] = request.user.active_farm.id
            data["created_by"] = request.user.id

        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_bulk_create(self, serializer):
        serializer.save()
