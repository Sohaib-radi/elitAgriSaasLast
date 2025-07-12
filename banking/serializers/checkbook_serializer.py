from rest_framework import serializers
from banking.models.checkbook import Checkbook

class CheckbookSerializer(serializers.ModelSerializer):
    """
    Serializer for Checkbook with clear validation and scalability.
    """

    class Meta:
        model = Checkbook
        fields = [
            "id",
            "bank",
            "start_number",
            "end_number",
            "issue_date",
            "status",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        start_number = attrs.get("start_number")
        end_number = attrs.get("end_number")
        if start_number and end_number and end_number < start_number:
            raise serializers.ValidationError({
                "end_number": "End check number must be greater than or equal to start check number."
            })
        return attrs
