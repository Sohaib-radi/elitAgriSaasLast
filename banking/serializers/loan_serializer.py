from rest_framework import serializers
from banking.models.loan import Loan

class LoanSerializer(serializers.ModelSerializer):
    """
    Serializer for the Loan model, providing clean validation and scalability.
    """

    class Meta:
        model = Loan
        fields = [
            "id",
            "bank",
            "loan_number",
            "loan_name",
            "amount",
            "interest_rate",
            "loan_duration",
            "start_date",
            "end_date",
            "repayment_method",
            "status",
            "description",
            "farm",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "farm", "created_by", "created_at", "updated_at"]


    def validate(self, attrs):
        """
        Cross-field validation for business rules.
        """
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date."
            })
        return attrs
