from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from animal.models.list import AnimalList
from animal.serializers.list import AnimalListSerializer
from core.viewsets.base import AutoPermissionViewSet


class AnimalListViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    Manage animal lists for the current farm.
    Centralized permission: animals.view / animals.manage
    """
    serializer_class = AnimalListSerializer
    permission_module = "animals"

    def get_queryset(self):
        return AnimalList.objects.filter(
            farm=self.request.user.active_farm,
            is_active=True
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                {"detail": "A list with this name already exists for this farm."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except (DjangoValidationError, DRFValidationError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"detail": f"Unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        serializer.save(
            farm=self.request.user.active_farm,
            created_by=self.request.user
        )
