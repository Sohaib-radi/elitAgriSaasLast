from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.serializers.user import UserMeSerializer
from django.contrib.auth.password_validation import validate_password
from core.models.user import User
from core.models.invite import InviteToken
from core.models.team import TeamMember
from django.utils import timezone
from core.models.user import User as CoreUser 

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        user = User.objects.get(id=user.id)  # Refresh from DB

        # Always ensure farm assignment is accurate
        team = TeamMember.objects.filter(user=user).first()

        if team:
            if user.active_farm != team.farm:
                print(f"[LOGIN DEBUG] Auto-assigning farm: {team.farm.name}")
                user.active_farm = team.farm
                user.save()
        else:
            if user.active_farm:
                print("[LOGIN DEBUG] Clearing active_farm – user removed from all teams.")
                user.active_farm = None
                user.save()

        self.context["user"] = user  # Set real user for use in view
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserMeSerializer(user, context=self.context).data,
        }


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        user.is_active = False  # User must be activated manually
        user.save()
        return user
    
    
class SwitchFarmSerializer(serializers.Serializer):
    farm_id = serializers.IntegerField()

    def validate_farm_id(self, value):
        user = self.context["request"].user

        if not TeamMember.objects.filter(user=user, farm_id=value).exists():
            raise serializers.ValidationError("You are not a member of this farm.")

        return value
    

class AcceptInviteSerializer(serializers.Serializer):
    """
    Accepts an invite using a secure token and activates the invited user.
    Sets password, full name, and links them to the farm with role and optional expiration.
    """
    token = serializers.UUIDField()
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            invite = InviteToken.objects.get(token=data['token'])
        except InviteToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid invite token."})

        if not invite.is_valid():
            raise serializers.ValidationError({"token": "This invite has expired or was already used."})

        data['invite'] = invite
        return data

    def save(self):
        invite = self.validated_data['invite']
        password = self.validated_data['password']
        full_name = self.validated_data['full_name']

        #  Activate the user and set their password
        user = User.objects.get(email=invite.email)
        user.set_password(password)
        user.full_name = full_name
        user.is_active = True
        user.save()

        # Link the user to the farm with role + expiration (if any)
        TeamMember.objects.get_or_create(
            user=user,
            farm=invite.farm,
            defaults={
                "role": invite.role,
                "is_admin": invite.is_admin,
                "expires_at": invite.expires_at,  #  Optional temp access
            }
        )

        #  Mark invite as used
        invite.used = True
        invite.save()

        return user