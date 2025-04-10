from rest_framework import serializers
from finance.models.purchase import PurchaseInvoice, PurchasePayment, PurchaseAttachment
from core.models.person import Person
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class PurchaseAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseAttachment
        fields = ["id", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(queryset=Person.objects.filter(type="supplier"), source="supplier", write_only=True)
    
    product_content_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(),
        source="product_content_type",
        write_only=True
    )
    product_object_id = serializers.IntegerField(write_only=True)

    attachments = PurchaseAttachmentSerializer(many=True, read_only=True)
    paid_amount = serializers.SerializerMethodField()

    remaining_amount = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model = PurchaseInvoice
        fields = [
            "id", "supplier", "supplier_id",
            "invoice_number", "product_content_type_id", "product_object_id",
            "quantity", "unit_price", "total_amount",
            "payment_method", "delivery_date", "address", "description",
            "attachments", "paid_amount", "remaining_amount",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "attachments", "paid_amount", "remaining_amount"]

    def create(self, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().create(validated_data)


class PurchasePaymentSerializer(serializers.ModelSerializer):
    invoice = serializers.PrimaryKeyRelatedField(queryset=PurchaseInvoice.objects.all())

    def validate_amount(self, value):
        invoice_id = self.initial_data.get("invoice")
        if invoice_id:
            invoice = PurchaseInvoice.objects.get(id=invoice_id)
            if value > invoice.remaining_amount:
                raise serializers.ValidationError(_("Payment exceeds the remaining amount."))
        return value

    class Meta:
        model = PurchasePayment
        fields = [
            "id", "invoice", "amount", "date", "note",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
