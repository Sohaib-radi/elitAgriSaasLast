from django.shortcuts import get_object_or_404
from core.viewsets.base import AutoPermissionViewSet
from animal.models.animal import Animal
from animal.serializers.animal import AnimalDetailSerializer, AnimalSerializer
from animal.filters.animal import AnimalFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from animal.serializers.animal import AnimalStatusSerializer
from animal.models.animal import AnimalStatus
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView

class AnimalDetailView(RetrieveAPIView):
    serializer_class = AnimalDetailSerializer
    permission_module = "animals"  
    def get_serializer_class(self):
        print("✅ USING AnimalDetailSerializer from VIEW")
        return AnimalDetailSerializer
    def get_queryset(self):
        return (
            Animal.objects
            .filter(farm=self.request.user.active_farm, is_active=True)
            .select_related("mother", "father")
        )
    
class AnimalViewSet(AutoPermissionViewSet):
    permission_module = "animals"
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnimalFilter

    def get_queryset(self):
        return (
            Animal.objects
            .filter(farm=self.request.user.active_farm, is_active=True)
            .select_related("mother", "father")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AnimalDetailSerializer
        return AnimalSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




class AnimalStatusListView(APIView):
    def get(self, request):
        status_data = [
            {"key": status.value, "label": status.label}
            for status in AnimalStatus
        ]
        return Response(AnimalStatusSerializer(status_data, many=True).data)


class AnimalDeleteView(APIView):
    permission_module = "animals"  
    def delete(self, request, pk):
        animal = get_object_or_404(Animal, pk=pk, farm=request.user.active_farm)

        # Optional: Soft delete instead of real delete
        animal.is_active = False
        animal.save()

        return Response({"detail": "Animal deleted successfully."}, status=status.HTTP_204_NO_CONTENT)