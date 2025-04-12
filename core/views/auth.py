from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.serializers.user import UserMeSerializer
from core.serializers.auth import LoginSerializer, SwitchFarmSerializer
from rest_framework import status
from core.serializers.auth import SignupSerializer
from core.models.farm import Farm
from core.models.team import TeamMember
from core.utils.audit import log_user_action
from core.serializers.auth import AcceptInviteSerializer
from core.permissions.permissions import IsNotExpired
from rest_framework.permissions import AllowAny
from farm_settings.models import FarmSettings
from core.constants.log_actions import LogActions
from django.utils.translation import gettext_lazy as _

class MeView(APIView):
    permission_classes = [IsAuthenticated,IsNotExpired]

    def get(self, request):
        serializer = UserMeSerializer(request.user, context={'request': request})
        return Response({"user": serializer.data})
    

class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    """
    🔐 Custom login that returns JWT + user profile + logs the action
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]
        user_data = serializer.validated_data["user"]

        # ✅ Real Django user object from serializer
        user = serializer.context.get("user")
        if not user:
            from core.models import User
            user = User.objects.get(email=serializer.initial_data['email'])

        # ✅ Log the login
        log_user_action(request, user, LogActions.LOGIN, user.active_farm)

        return Response({
            "access": access,
            "refresh": refresh,
            "user": user_data
        }, status=status.HTTP_200_OK)


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Account created. Awaiting admin approval.")}, status=status.HTTP_201_CREATED)

class SwitchFarmView(APIView):
    """
     Allows a user to switch their active farm context, only if multi-farm is enabled.
    """
    permission_classes = [IsAuthenticated, IsNotExpired]

    def post(self, request):
        serializer = SwitchFarmSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        farm_id = serializer.validated_data["farm_id"]

        user = request.user
        from core.models import Farm
        farm = Farm.objects.get(id=farm_id)

        #  Check if multi-farm is allowed in the current active farm
        current_farm = user.active_farm
        if current_farm:
            settings = getattr(current_farm, "settings", None)
            if settings and not settings.multi_farm_enabled:
                return Response({"detail": _("Multi-farm switching is disabled for this farm.")}, status=403)

        # Set new farm
        user.active_farm = farm
        user.save()

        log_user_action(request, user,LogActions.SWITCH_FARM, farm)

        return Response({
            "detail": f"Switched to farm: {farm.name}",
            "user": UserMeSerializer(user, context={"request": request}).data
        })

# Accept invite and activate user account from secure token
    # Open an Accept Invite Form
    # Pre-fill the user’s email (if needed)
    # Let the user set a password + full name
    # Then call the backend /auth/accept-invite/ endpoint

class AcceptInviteView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = AcceptInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"detail": _("Account activated successfully.")}, status=status.HTTP_200_OK)



class MyFarmsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        farms = (
            TeamMember.objects
            .filter(user=request.user)
            .select_related("farm")
            .values("farm__id", "farm__name")
        )
        return Response([
            {"id": f["farm__id"], "name": f["farm__name"]} for f in farms
        ])