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
    email = serializers.EmailField(source='user.email', read_only=True)
    name = serializers.CharField(source='user.full_name', read_only=True)
    phoneNumber = serializers.CharField(source='user.phone', read_only=True)
    isVerified = serializers.BooleanField(source='user.is_active', read_only=True)
    city = serializers.CharField(source='user.city', read_only=True)
    state = serializers.CharField(source='user.state', read_only=True)
    status = serializers.SerializerMethodField() 
    address = serializers.CharField(source='user.address', read_only=True)
    country = serializers.CharField(source='user.country', read_only=True)
    zipCode = serializers.CharField(source='user.zip_code', read_only=True)
    company = serializers.CharField(source='user.company', read_only=True)
    avatarUrl = serializers.CharField(source='user.avatar_url', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    role = serializers.SerializerMethodField()
    farm = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = [
            'id', 'email', 'name', 'phoneNumber', 'isVerified', 'city', 'state', 'status',
            'address', 'country', 'zipCode', 'company', 'avatarUrl','avatar', 'role', 'is_admin', 'farm'
        ]

    def get_status(self, obj):
        return obj.user.status  # ✅ safely calls the @property from the User model

    def get_role(self, obj):
        if obj.role:
            return {
                "id": obj.role.id,
                "name": obj.role.name,
            }
        return ""

    def get_farm(self, obj):
        if obj.farm:
            return {
                "id": obj.farm.id,
                "name": obj.farm.name,
            }
        return None


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