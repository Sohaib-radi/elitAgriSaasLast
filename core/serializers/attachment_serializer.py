from rest_framework import serializers
from core.models.attachment import Attachment
from django.contrib.contenttypes.models import ContentType

class AttachmentSerializer(serializers.ModelSerializer):
    """
    Professional serializer for Attachment supporting multi-model usage.
    """

    content_type = serializers.SlugRelatedField(
        slug_field="model",
        queryset=ContentType.objects.all(),
        help_text="Model name of the related object (e.g., banktransaction, loanpayment)."
    )
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Attachment
        fields = [
            "id",
            "content_type",
            "object_id",
            "name",
            "file",
            "file_type",
            "extension",
            "size",
            "uploaded_by",
            "description",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "file_type", "extension", "size", "uploaded_by", "created_at", "updated_at"]

    def validate_file(self, value):
        max_size = 20 * 1024 * 1024  # 20 MB
        if value.size > max_size:
            raise serializers.ValidationError("File size exceeds the 20MB limit.")
        return value

    def validate(self, attrs):
        content_type = attrs.get("content_type")
        object_id = attrs.get("object_id")
        if content_type and object_id:
            model_class = content_type.model_class()
            if not model_class.objects.filter(id=object_id).exists():
                raise serializers.ValidationError({
                    "object_id": "The referenced object does not exist."
                })
        return attrs
