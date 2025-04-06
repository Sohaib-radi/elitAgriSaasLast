from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from animal.models.animal import Animal
from animal.serializers.media import AnimalImageUploadSerializer
from core.permissions.mixins import AutoPermissionMixin


class AnimalImageUploadView(AutoPermissionMixin, APIView):
    """
    Upload animal image.
    Requires: custom permission `animals.manage`
    """
    permission_module = "animals"  # 👈 matches registry key

    def post(self, request, pk):
        animal = get_object_or_404(Animal, pk=pk, farm=request.user.active_farm)

        serializer = AnimalImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(animal=animal, created_by=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
