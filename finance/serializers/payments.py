from rest_framework import serializers
from finance.models.payment import Payment
from finance.models.receipt import Receipt
from core.models.person import Person
from finance.models.payment_attachment import PaymentAttachment
from finance.models.receipt_attachment import ReceiptAttachment
from django.utils.translation import gettext_lazy as _
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["person_id"].queryset = self.get_person_queryset()

    def get_person_queryset(self):
        user = self.context["request"].user
        return Person.objects.filter(farm=user.active_farm)

    person_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.none(), source="person", write_only=True
    )

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Amount must be greater than 0."))
        return value
    def update(self, instance, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().update(instance, validated_data)
    class Meta:
        model = Receipt
        fields = [
            "id", "person", "person_id",
            "receipt_number", "amount", "date",
            "description", "attachments",
            "accountant_signature", "recipient_signature",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "person", "attachments"]

    def create(self, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().create(validated_data)

class PaymentSerializer(serializers.ModelSerializer):
    person = PersonInfoSerializer(read_only=True)
    attachments = PaymentAttachmentSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["person_id"].queryset = self.get_person_queryset()

    def get_person_queryset(self):
        user = self.context["request"].user
        return Person.objects.filter(farm=user.active_farm)

    person_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.none(), source="person", write_only=True
    )

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Amount must be greater than 0."))
        return value
    
    def update(self, instance, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().update(instance, validated_data)
    
    class Meta:
        model = Payment
        fields = [
            "id", "person", "person_id",
            "payment_number", "amount", "date", "attachments",
            "description", "accountant_signature", "recipient_signature",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "person", "attachments"]

    def create(self, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().create(validated_data)
