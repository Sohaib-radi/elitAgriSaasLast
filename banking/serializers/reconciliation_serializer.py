from rest_framework import serializers
from banking.models.reconciliation import Reconciliation

class ReconciliationSerializer(serializers.ModelSerializer):
    """
    Serializer for Reconciliation with clean validation and structure.
    """

    class Meta:
        model = Reconciliation
        fields = [
            "id",
            "bank_transaction",
            "loan_payment",
            "linked_check",
            "reconciled_amount",
            "status",
            "reconciliation_date",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "reconciliation_date"]

    def validate(self, attrs):
        reconciled_amount = attrs.get("reconciled_amount")
        if reconciled_amount and reconciled_amount <= 0:
            raise serializers.ValidationError({
                "reconciled_amount": "Reconciled amount must be greater than zero."
            })
        return attrs
