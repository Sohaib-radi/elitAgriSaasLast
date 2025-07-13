from rest_framework import serializers
from banking.models.loan import Loan

class LoanSerializer(serializers.ModelSerializer):
    """
    Serializer for the Loan model, providing clean validation and scalability.
    """
    bank_name = serializers.CharField(source="bank.name", read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "bank",
            "bank_name",
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

    def validate_loan_duration(self, value):
        if value < 2:
            raise serializers.ValidationError("Loan duration must be at least 2 months.")
        return value
    def validate_interest_rate(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Interest rate must be between 0% and 100%.")
        return value
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
