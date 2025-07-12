from rest_framework import serializers
from banking.models.bank_transaction import BankTransaction

class BankTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for BankTransaction with validation and clear structure.
    """

    class Meta:
        model = BankTransaction
        fields = [
            "id",
            "bank",
            "transaction_date",
            "amount",
            "transaction_type",
            "payment_method",
            "reference",
            "loan",
            "status",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Transaction amount must be greater than zero.")
        return value

    def validate(self, attrs):
        if attrs.get("transaction_type") == "loan_payment" and not attrs.get("loan"):
            raise serializers.ValidationError({
                "loan": "Loan must be specified for loan payment transactions."
            })
        return attrs
