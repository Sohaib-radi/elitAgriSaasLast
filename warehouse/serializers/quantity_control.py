from rest_framework import serializers
from warehouse.models.quantity_control import WarehouseQuantitySchedule, WarehouseReminder
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

class WarehouseQuantityScheduleSerializer(serializers.ModelSerializer):
    reference_content_type = serializers.SlugRelatedField(
        slug_field="model",
        queryset=ContentType.objects.all(),
        source="content_type"
    )
    reference_id = serializers.IntegerField(source="object_id")

    class Meta:
        model = WarehouseQuantitySchedule
        fields = [
            "id",
            "warehouse",
            "reference_content_type",
            "reference_id",
            "action",
            "frequency",
            "amount",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def validate(self, data):
        model_class = data["content_type"].model_class()
        object_id = data["object_id"]

        try:
            model_class.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"reference_id": _("The referenced object does not exist.")})

        if data["amount"] <= 0:
            raise serializers.ValidationError({"amount": _("Amount must be greater than zero.")})
        return data

class WarehouseReminderSerializer(serializers.ModelSerializer):
    reference_content_type = serializers.SlugRelatedField(
        slug_field="model",
        queryset=ContentType.objects.all(),
        source="content_type"
    )
    reference_id = serializers.IntegerField(source="object_id")

    class Meta:
        model = WarehouseReminder
        fields = [
            "id",
            "warehouse",
            "reference_content_type",
            "reference_id",
            "alert_quantity",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def validate(self, data):
        model_class = data["content_type"].model_class()
        object_id = data["object_id"]

        try:
            model_class.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"reference_id": _("The referenced object does not exist.")})

        if data["alert_quantity"] <= 0:
            raise serializers.ValidationError({"alert_quantity": _("Alert quantity must be greater than zero.")})
        return data
