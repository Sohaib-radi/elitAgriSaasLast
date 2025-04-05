from rest_framework import serializers
from core.models.audit import UserLog
from core.serializers.user import UserSimpleSerializer
from core.serializers.farm import FarmSerializer

class UserLogSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    farm = FarmSerializer()

    class Meta:
        model = UserLog
        fields = ['id', 'user', 'action', 'farm', 'ip_address', 'user_agent', 'created_at']
