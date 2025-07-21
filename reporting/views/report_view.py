from rest_framework import viewsets, permissions
from reporting.models.report import ReportRecord
from reporting.serializers.report_serializer import ReportRecordSerializer

class ReportRecordViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to list all report records for the current user's farm.
    """
    queryset = ReportRecord.objects.all().select_related("created_by")
    serializer_class = ReportRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(created_by=user).order_by("-created_at")
