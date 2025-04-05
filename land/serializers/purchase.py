from rest_framework import serializers
from land.models.purchase import LandPurchase, TransactionType


class LandPurchaseSerializer(serializers.ModelSerializer):
    land_number = serializers.CharField(source="land.land_number", read_only=True)

    class Meta:
        model = LandPurchase
        fields = [
            "id",
            "land",
            "land_number",
            "transaction_type",
            "buyer",
            "seller_name",
            "seller_contact",
            "purchase_price",
            "purchase_date",
            "notes",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "land_number"]
