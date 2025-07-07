from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from rest_framework import status

ALLOWED_MODELS = ["product", "crop", "animal", "newbornanimal"]

class WarehouseContentTypeListView(APIView):
    """
    Returns allowed content types for warehouse entries for frontend dropdown selection.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content_types = ContentType.objects.filter(model__in=ALLOWED_MODELS)
        result = [
            {
                "id": ct.id,
                "model": ct.model,
                "app_label": ct.app_label,
                "verbose_name": ct.model_class()._meta.verbose_name.title() if ct.model_class() else ct.model
            }
            for ct in content_types
        ]
        return Response(result)
