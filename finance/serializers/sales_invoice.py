from rest_framework import serializers
from finance.models.sales_invoice import SalesInvoice
from core.models.person import Person
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class SalesInvoiceSerializer(serializers.ModelSerializer):
    buyer = serializers.SerializerMethodField()
    buyer_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.filter(type="client"), source="buyer", write_only=True
    )

    content_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(), source="content_type", write_only=True
    )

    product_label = serializers.SerializerMethodField()

    def get_buyer(self, obj):
        return {
            "id": obj.buyer.id,
            "name": obj.buyer.name,
            "type": obj.buyer.type,
        }

    def get_product_label(self, obj):
        try:
            return str(obj.product_object)
        except:
            return None

    def validate(self, data):
        if data["quantity"] <= 0:
            raise serializers.ValidationError({"quantity": _("Quantity must be greater than zero.")})
        if data["unit_price"] <= 0:
            raise serializers.ValidationError({"unit_price": _("Unit price must be greater than zero.")})
        return data

    def create(self, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().update(instance, validated_data)

    class Meta:
        model = SalesInvoice
        fields = [
            "id", "buyer", "buyer_id",
            "invoice_number", "content_type_id", "object_id", "product_label",
            "location", "address", "phone", "date",
            "quantity", "unit_price", "total_amount",
            "payment_method", "delivery_date", "vat",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "buyer", "product_label"]
