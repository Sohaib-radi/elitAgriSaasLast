from rest_framework import serializers
from product_catalogue.models.personal_product import PersonalProduct

class PersonalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProduct
        fields = [
            "id",
            "project",
            "product",
            "quantity",
            "notes",
            "created_at",
            "created_by",
        ]
        read_only_fields = ["id", "created_at", "created_by"]
