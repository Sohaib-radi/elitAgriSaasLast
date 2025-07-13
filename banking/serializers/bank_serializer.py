from rest_framework import serializers
from banking.models.bank import Bank

class BankSerializer(serializers.ModelSerializer):
    """
    Serializer for Bank model, providing clean validation, scalability, and clarity for Elit Agri.
    """
    main_currency_name = serializers.SerializerMethodField()
    class Meta:
        model = Bank
        fields = [
            "id",
            "name",
            "bank_number",
            "branch",
            "account_number",
            "iban",
            "swift_code",
            "address",
            "phone_number",
            "email",
            "main_currency",
            "main_currency_name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_main_currency_name(self, obj):
        return obj.main_currency.code if obj.main_currency else None
    
    def validate_account_number(self, value):
        """
        Ensure account number uniqueness within the same bank number context.
        """
        if self.instance:
            if Bank.objects.exclude(id=self.instance.id).filter(account_number=value).exists():
                raise serializers.ValidationError("Account number must be unique.")
        else:
            if Bank.objects.filter(account_number=value).exists():
                raise serializers.ValidationError("Account number must be unique.")
        return value

    def validate(self, attrs):
        """
        Additional cross-field validation if needed.
        """
        # Example: if SWIFT is provided, IBAN must also be provided
        if attrs.get("swift_code") and not attrs.get("iban"):
            raise serializers.ValidationError({
                "iban": "IBAN is required when SWIFT code is provided."
            })
        return attrs
