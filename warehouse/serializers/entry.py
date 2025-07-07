from rest_framework import serializers
from warehouse.models.entry import WarehouseEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

class WarehouseEntrySerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all()
    )
    object_id = serializers.IntegerField()
    content_object = serializers.SerializerMethodField(read_only=True)
    reference_name = serializers.SerializerMethodField(read_only=True)
    model_type = serializers.SerializerMethodField(read_only=True)
    content_type_verbose = serializers.SerializerMethodField(read_only=True)
    def get_content_type_verbose(self, obj):
        try:
            return obj.content_type.model_class()._meta.verbose_name.title()
        except:
            return obj.model_type.capitalize()
    class Meta:
        model = WarehouseEntry
        fields = [
            "id",
            "warehouse",
            "content_type",
            "object_id",
            "content_object",
            "reference_name",
            "model_type",
            "content_type_verbose",
            "quantity",
            "weight",
            "space_taken",
            "entry_presence",
            "status",
            "origin",
            "notes",
            "barcode",
            "date_added",
            "is_active",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "date_added",
            "content_object",
            "reference_name",
            "model_type",
            "created_at",
            "updated_at",
            "created_by",
        ]

    def validate(self, data):
        model_class = data["content_type"].model_class()
        try:
            model_class.objects.get(pk=data["object_id"])
        except model_class.DoesNotExist:
            raise serializers.ValidationError(
                {"object_id": _("The referenced object does not exist.")}
            )
        return data

    def get_content_object(self, obj):
        try:
            return str(obj.content_object)
        except Exception:
            return None

    def get_reference_name(self, obj):
        return obj.reference_name()

    def get_model_type(self, obj):
        return obj.model_type
