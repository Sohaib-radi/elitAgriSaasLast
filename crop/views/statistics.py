# crop/views/statistics.py

from crop.models.crop import Crop
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions.permissions import IsNotExpired, HasRolePermission
from crop.serializers.statistics import CropStatisticsSerializer


class CropStatisticsView(APIView):
    permission_module = "crop"

    def post(self, request):
        serializer = CropStatisticsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filters = {"farm": request.user.active_farm}

        data = serializer.validated_data

        if data.get("from_date"):
            filters["date__gte"] = data["from_date"]
        if data.get("to_date"):
            filters["date__lte"] = data["to_date"]
        if data.get("usage"):
            filters["usage"] = data["usage"]
        if data.get("wilaya_id"):
            filters["agricultural_land__land__wilaya_id"] = data["wilaya_id"]

        stats = (
            Crop.objects.filter(**filters)
            .values("crop_type", "unit")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("crop_type")
        )

        return Response(stats)
