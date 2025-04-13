from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

from core.models.team import TeamMember
from core.models.invite import InviteToken
from core.serializers.team import (
    TeamMemberCreateSerializer,
    TeamMemberListSerializer,
    TeamMemberInviteSerializer,
    TeamMemberUpdateSerializer
)
from core.viewsets.base import AutoPermissionAPIView

User = get_user_model()


class TeamMemberView(AutoPermissionAPIView):
    permission_module = "team"

    def get(self, request):
        farm = request.user.active_farm
        team = TeamMember.objects.filter(farm=farm)
        serializer = TeamMemberListSerializer(team, many=True)
        return Response(serializer.data)

    def post(self, request):
        farm = request.user.active_farm
        serializer = TeamMemberCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Team member added successfully.")})


class TeamMemberInviteView(AutoPermissionAPIView):
    permission_module = "team"

    def post(self, request):
        farm = request.user.active_farm
        serializer = TeamMemberInviteSerializer(data=request.data, context={'farm': farm})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("User invited and added to the farm.")}, status=status.HTTP_201_CREATED)


class TeamMemberDetailView(AutoPermissionAPIView):
    permission_module = "team"

    def get(self, request, pk):
        farm = request.user.active_farm
        member = get_object_or_404(TeamMember, pk=pk, farm=farm)
        serializer = TeamMemberListSerializer(member)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        farm = request.user.active_farm
        member = get_object_or_404(TeamMember, pk=pk, farm=farm)

        serializer = TeamMemberUpdateSerializer(member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Team member updated.")})

    def delete(self, request, pk):
        farm = request.user.active_farm
        member = get_object_or_404(TeamMember, pk=pk, farm=farm)
        member.delete()
        return Response({"detail": _("Team member removed.")}, status=204)


class InviteUserView(AutoPermissionAPIView):
    permission_module = "team"

    def post(self, request):
        farm = request.user.active_farm

        serializer = TeamMemberInviteSerializer(data=request.data, context={"farm": farm})
        serializer.is_valid(raise_exception=True)

        member = serializer.save()
        try:
        # Generate invite URL
            token = InviteToken.objects.create(
                email=member.user.email,
                farm=farm,
                role=member.role,
                is_admin=member.is_admin,
                # optional
                expires_at=member.expires_at  
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=500)

        invite_url = f"{settings.FRONTEND_URL}/accept-invite/?token={token.token}"

        return Response({
            "detail": _("User invited and added to the farm."),
            "invite_url": invite_url
        }, status=201)
