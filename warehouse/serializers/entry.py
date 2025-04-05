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

    class Meta:
        model = WarehouseEntry
        fields = [
            "id",
            "warehouse",
            "content_type",
            "object_id",
            "content_object",
            "quantity",
            "weight",
            "space_taken",
            "entry_presence",
            "date_added",
        ]
        read_only_fields = ["id", "date_added", "content_object"]

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
        except:
            return None

