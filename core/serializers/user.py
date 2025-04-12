# core/serializers/user.py

from rest_framework import serializers
from core.models.user import User
from core.models.team import TeamMember
from core.models.role import Role
from core.models.farm import Farm


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']

        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'name']

class UserMeSerializer(serializers.ModelSerializer):
    farm = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    # ➕ Additional mappings for frontend
    name = serializers.CharField(source='full_name')
    phoneNumber = serializers.CharField(source='phone')
    isVerified = serializers.BooleanField(source='is_active')

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'phoneNumber', 'isVerified',
            'city', 'state', 'status', 'address', 'country', 'zip_code',
            'company', 'avatar_url', 'farm', 'role', 'is_admin'
        ]

    def get_farm(self, user):
        if not user.active_farm:
            return None
        return FarmSerializer(user.active_farm).data

    def get_role(self, user):
        if not user.active_farm:
            return None
        team = TeamMember.objects.filter(user=user, farm=user.active_farm).first()
        return RoleSerializer(team.role).data if team and team.role else None

    def get_is_admin(self, user):
        if not user.active_farm:
            return False
        team = TeamMember.objects.filter(user=user, farm=user.active_farm).first()
        return team.is_admin if team else False