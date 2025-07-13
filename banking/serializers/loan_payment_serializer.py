from rest_framework import serializers
from banking.models.loan_payment import LoanPayment

class LoanPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for LoanPayment with clear structure and validation.
    """
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = LoanPayment
        fields = [
            "id",
            "loan",
            "payment_date",
            "farm",
            "amount_paid",
            "principal_paid",
            "interest_paid",
            "remaining_balance",
            "payment_method",
            "payment_method_display",
            "payment_reference",
            "status",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at","farm", "updated_at"]

    def validate(self, attrs):
        principal = attrs.get("principal_paid", 0)
        interest = attrs.get("interest_paid", 0)
        total = attrs.get("amount_paid", 0)
        if total != principal + interest:
            raise serializers.ValidationError({
                "amount_paid": "Total paid must equal the sum of principal and interest."
            })
        return attrs
