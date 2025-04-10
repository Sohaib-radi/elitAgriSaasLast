from rest_framework import serializers
from finance.models.debt import Debt, DebtAttachment
from core.models.person import Person
from django.utils.translation import gettext_lazy as _


class DebtAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtAttachment
        fields = ["id", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class PersonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "name", "type"]


class DebtSerializer(serializers.ModelSerializer):
    person = PersonInfoSerializer(read_only=True)
    attachments = DebtAttachmentSerializer(many=True, read_only=True)

    person_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.none(), source="person", write_only=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["person_id"].queryset = self.get_person_queryset()

    def get_person_queryset(self):
        user = self.context["request"].user
        return Person.objects.filter(farm=user.active_farm)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Amount must be greater than zero."))
        return value

    def create(self, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["farm"] = self.context["request"].user.active_farm
        return super().update(instance, validated_data)

    class Meta:
        model = Debt
        fields = [
            "id", "person", "person_id", "amount", "reason", "due_date",
            "status", "description", "attachments",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "attachments", "person"]
