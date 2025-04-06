from rest_framework import serializers
from finance.models.payment import Payment
from finance.models.receipt import Receipt
from core.models.person import Person
from finance.models.payment_attachment import PaymentAttachment
from finance.models.receipt_attachment import ReceiptAttachment

class PersonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "name", "type"]

class PaymentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAttachment
        fields = ["id", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

class ReceiptAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptAttachment
        fields = ["id", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

class ReceiptSerializer(serializers.ModelSerializer):
    person = PersonInfoSerializer(read_only=True)
    attachments = ReceiptAttachmentSerializer(many=True, read_only=True)
    person_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(), source="person", write_only=True
    )

    class Meta:
        model = Receipt
        fields = [
            "id", "person", "person_id",
            "receipt_number", "amount", "date",
            "description","attachments", "accountant_signature", "recipient_signature",
            "created_at", "updated_at", "farm"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "person","attachments"]


class PaymentSerializer(serializers.ModelSerializer):
    person = PersonInfoSerializer(read_only=True)
    attachments = PaymentAttachmentSerializer(many=True, read_only=True)
    person_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(), source="person", write_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id", "person", "person_id",
            "payment_number", "amount", "date","attachments",
            "description", "accountant_signature", "recipient_signature",
            "created_at", "updated_at", "farm"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "person","attachments"]
