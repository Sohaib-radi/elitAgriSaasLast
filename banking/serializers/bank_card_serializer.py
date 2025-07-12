from rest_framework import serializers
from banking.models.bank_card import BankCard

class BankCardSerializer(serializers.ModelSerializer):
    """
    Serializer for BankCard with clean validation.
    """

    class Meta:
        model = BankCard
        fields = [
            "id",
            "bank",
            "card_type",
            "card_number",
            "holder_name",
            "issue_date",
            "expiry_date",
            "card_limit",
            "status",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_card_number(self, value):
        if BankCard.objects.filter(card_number=value).exists():
            raise serializers.ValidationError("Card number must be unique.")
        return value

    def validate(self, attrs):
        expiry_date = attrs.get("expiry_date")
        issue_date = attrs.get("issue_date")
        if expiry_date and issue_date and expiry_date <= issue_date:
            raise serializers.ValidationError({
                "expiry_date": "Expiry date must be after issue date."
            })
        return attrs
