# core/serializers/user.py

from rest_framework import serializers
from core.models.user import User
from core.models.team import TeamMember
from core.models.role import Role
from core.models.farm import Farm
from django.utils.translation import gettext_lazy as _

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
    status = serializers.ReadOnlyField()  

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'phoneNumber', 'isVerified',
            'city', 'state', 'status', 'address', 'country', 'zip_code',
            'company', 'avatar_url', 'avatar', 'farm', 'role', 'is_admin'
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

    

class UserCreateUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    # New writable fields
    role = serializers.CharField(required=False)
    is_admin = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'email', 'full_name', 'phone', 'avatar_url', 'avatar', 'address',
            'city', 'state', 'country', 'zip_code', 'company',
            'is_active', 'is_verified',
            'role', 'is_admin',
        ]

    def validate_email(self, value):
        if self.instance is None and not value:
            raise serializers.ValidationError(_("Email is required."))
        return value

    def validate_full_name(self, value):
        if self.instance is None and not value:
            raise serializers.ValidationError(_("Full name is required."))
        return value

    def update(self, instance, validated_data):
        role_name = validated_data.pop('role', None)
        is_admin = validated_data.pop('is_admin', None)

        user = super().update(instance, validated_data)

        # ✅ Use team_member from context (not refetching from DB)
        team_member = self.context.get("team_member")

        if role_name and team_member:
            try:
                role_obj = Role.objects.get(name=role_name)
                team_member.role = role_obj
                if is_admin is not None:
                    team_member.is_admin = is_admin
                team_member.save()
            except Role.DoesNotExist:
                raise serializers.ValidationError({"role": _("Invalid role name.")})

        return user