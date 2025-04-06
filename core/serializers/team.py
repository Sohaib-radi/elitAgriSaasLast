from rest_framework import serializers
from core.models.team import TeamMember
from core.models.user import User
from core.models.role import Role
from core.models.farm import Farm
from django.contrib.auth import get_user_model


User = get_user_model()

class TeamMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['user', 'role', 'is_admin']

    def validate_user(self, user):
        farm = self.context['request'].user.team_assignments.first().farm
        if TeamMember.objects.filter(user=user, farm=farm).exists():
            raise serializers.ValidationError("User is already in this farm.")
        return user

    def create(self, validated_data):
        farm = self.context['request'].user.team_assignments.first().farm
        return TeamMember.objects.create(farm=farm, **validated_data)


class TeamMemberListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'user_email', 'full_name', 'role_name', 'is_admin', 'created_at']


class TeamMemberInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=255)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    is_admin = serializers.BooleanField(default=False)

    def validate_email(self, email):
        # Avoid duplicates
        farm = self.context['farm']
        user = User.objects.filter(email=email).first()
        if user and TeamMember.objects.filter(user=user, farm=farm).exists():
            raise serializers.ValidationError("User already assigned to this farm.")
        return email
      

    def create(self, validated_data):
        email = validated_data['email']
        full_name = validated_data['full_name']
        role = validated_data['role']
        is_admin = validated_data['is_admin']
        farm = self.context['farm']

        # Create or get user
        user, created = User.objects.get_or_create(email=email, defaults={
            'full_name': full_name,
            'is_active': True
        })

        # Assign to team
        return TeamMember.objects.create(
            user=user,
            farm=farm,
            role=role,
            is_admin=is_admin
        )


class TeamMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['role', 'is_admin']