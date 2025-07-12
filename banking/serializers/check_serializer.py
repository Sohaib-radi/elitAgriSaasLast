from rest_framework import serializers
from banking.models.check import Check

class CheckSerializer(serializers.ModelSerializer):
    """
    Serializer for Check with validation and clean structure.
    """

    class Meta:
        model = Check
        fields = [
            "id",
            "checkbook",
            "check_number",
            "issue_date",
            "due_date",
            "amount",
            "beneficiary_name",
            "status",
            "payment_status",
            "transaction",
            "direction",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        issue_date = attrs.get("issue_date")
        due_date = attrs.get("due_date")
        if due_date and issue_date and due_date < issue_date:
            raise serializers.ValidationError({
                "due_date": "Due date must be after or equal to issue date."
            })
        return attrs
