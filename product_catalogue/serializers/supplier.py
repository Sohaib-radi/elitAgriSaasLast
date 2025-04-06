# product_catalogue/serializers/supplier.py

from rest_framework import serializers
from product_catalogue.models.supplier import SupplierList, Supplier
from product_catalogue.serializers.product import ProductSerializer

class SupplierListSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        farm = self.context["request"].user.active_farm
        # Exclude current instance from check if updating
        qs = SupplierList.objects.filter(farm=farm, name=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("A supplier list with this name already exists for your farm.")
        return value

    class Meta:
        model = SupplierList
        fields = ["id", "name", "created_by", "created_at","description"]
        read_only_fields = ["id", "created_by", "created_at"]

class SupplierSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier._meta.get_field("product").related_model.objects.all(),
        source="product",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Supplier
        fields = [
            "id", "supplier_name", "company_name", "phone_number", "address",
            "product", "product_id", "product_type", "price", "payment_method",
            "notes", "image", "list", "farm", "created_by", "created_at"
        ]
        read_only_fields = ["id", "created_by", "created_at", "farm"]
