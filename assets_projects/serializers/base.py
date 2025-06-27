from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class FarmScopedSerializer(serializers.ModelSerializer):
    def validate(self, data):
        data['farm'] = self.context['request'].user.active_farm
        return data

    def get_queryset(self):
        return super().get_queryset().filter(
            farm=self.context['request'].user.active_farm
        )