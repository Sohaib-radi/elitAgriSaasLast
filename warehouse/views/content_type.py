from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from rest_framework import status

ALLOWED_MODELS = ["product", "crop", "animal", "newbornanimal"]
class WarehouseContentTypeListView(APIView):
    """
    Return allowed content types for warehouse entries.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content_types = ContentType.objects.filter(model__in=ALLOWED_MODELS)
        result = [
            {
                "id": ct.id,
                "model": ct.model,
                "app_label": ct.app_label
            }
            for ct in content_types
        ]
        return Response(result)