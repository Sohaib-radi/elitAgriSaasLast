from rest_framework import serializers
from reporting.models.report import ReportRecord

class ReportRecordSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.get_full_name", read_only=True)
    file_url = serializers.FileField(source="file_path", read_only=True)

    class Meta:
        model = ReportRecord
        fields = [
            "id", "name", "type", "status", "created_by_name",
            "filters", "file_url", "executed_at", "created_at"
        ]
