from rest_framework import serializers
from farm_settings.models import Currency, FarmCurrency, CurrencyRate


class CurrencySerializer(serializers.ModelSerializer):
    """
    Read-only serializer for global currencies (e.g., USD, EUR)
    """

    class Meta:
        model = Currency
        fields = ["id", "code", "name"]
        read_only_fields = fields


class FarmCurrencySerializer(serializers.ModelSerializer):
    """
    Serializer for currencies added to a specific farm
    """
    currency = CurrencySerializer(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        source="currency",
        write_only=True,
    )

    class Meta:
        model = FarmCurrency
        fields = [
            "id",
            "currency",
            "currency_id",
            "is_active",
            "created_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "created_by"]


class CurrencyRateSerializer(serializers.ModelSerializer):
    """
    Serializer for exchange rate values by date
    """
    class Meta:
        model = CurrencyRate
        fields = [
            "id",
            "farm_currency",
            "date",
            "rate",
            "created_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "created_by"]
