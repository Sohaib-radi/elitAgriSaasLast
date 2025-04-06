from rest_framework import serializers
from warehouse.models.quantity_control import WarehouseQuantitySchedule, WarehouseReminder
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

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
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate(self, data):
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
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate_alert_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Alert quantity must be greater than zero."))
        return value
