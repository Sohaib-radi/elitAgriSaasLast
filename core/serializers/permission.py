from rest_framework import serializers
from core.models.permissions import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["code", "label"]
