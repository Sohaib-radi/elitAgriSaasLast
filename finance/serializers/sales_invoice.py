from rest_framework import serializers
from finance.models.sales_invoice import SalesInvoice, SalesInvoiceItem
from core.models.person import Person
from django.utils.translation import gettext_lazy as _

class SalesInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoiceItem
        fields = [
            "id", "title", "description", "quantity", "price", "total", "created_at", "updated_at", "service",
        ]
        read_only_fields = ["id", "total", "created_at", "updated_at"]

class SalesInvoiceSerializer(serializers.ModelSerializer):
    buyer = serializers.SerializerMethodField(read_only=True)
    buyer_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.filter(type="client"),
        source="buyer",
        write_only=True
    )
    items = SalesInvoiceItemSerializer(many=True, required=True)

    def get_buyer(self, obj):
        if obj.buyer:
            return {
                "id": obj.buyer.id,
                "name": obj.buyer.name,
                "type": obj.buyer.type,
            }
        return None

    def validate(self, data):
        # Additional validations if needed
        return data

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        validated_data["farm"] = self.context["request"].user.active_farm
        invoice = SalesInvoice.objects.create(**validated_data)

        for item_data in items_data:
            SalesInvoiceItem.objects.create(invoice=invoice, **item_data)

        invoice.update_totals()
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])
        validated_data["farm"] = self.context["request"].user.active_farm

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data:
            # Simple strategy: clear and recreate items
            instance.items.all().delete()
            for item_data in items_data:
                SalesInvoiceItem.objects.create(invoice=instance, **item_data)

        instance.update_totals()
        return instance

    class Meta:
        model = SalesInvoice
        fields = [
            "id", "buyer", "buyer_id",
            "invoice_number", "location", "address", "phone",
            "date", "delivery_date", "payment_method", "status",
            "subtotal", "discount", "shipping", "taxes", "vat", "total_amount",
            "invoice_from", "invoice_to",
            "items",
            "created_at", "updated_at"
        ]
        read_only_fields = [
            "id", "subtotal", "total_amount", "created_at", "updated_at", "buyer"
        ]
