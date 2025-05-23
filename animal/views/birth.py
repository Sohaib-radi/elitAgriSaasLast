from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from core.viewsets.base import AutoPermissionViewSet
from core.permissions.permissions import IsNotExpired, HasRolePermission
from rest_framework.permissions import IsAuthenticated
from animal.models.birth import AnimalBirth
from animal.serializers.birth import AnimalBirthSerializer
from animal.serializers.animal import AnimalSerializer
from animal.filters.birth import AnimalBirthFilter
from animal.services.birth_transfer import move_birth_to_animal
from animal.services.vaccine_suggestion import suggest_vaccines_for_birth


class AnimalBirthViewSet(AutoPermissionViewSet):
    """
    Manage animal birth records
    """
    serializer_class = AnimalBirthSerializer
    permission_module = "animal_births"
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnimalBirthFilter

    def get_queryset(self):
        return AnimalBirth.objects.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        birth = serializer.save(
            farm=self.request.user.active_farm,
            created_by=self.request.user
        )
        suggestions = suggest_vaccines_for_birth(birth)
        print("Suggested vaccines:", suggestions)


class MoveBirthToAnimalView(APIView):
    """
    Moves a birth record to Animal after validation
    """
    permission_module = "animal_births"

    def post(self, request, pk):
        birth = get_object_or_404(AnimalBirth, pk=pk, farm=request.user.active_farm)

        try:
            animal = move_birth_to_animal(birth)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
