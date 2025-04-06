from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.serializers.permission import PermissionSerializer
from core.models.team import TeamMember
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class MyPermissionsView(APIView):
    """
     Return the current user's permissions based on their active farm and role.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        farm = getattr(user, "active_farm", None)

        if not farm:
            return Response({"detail": _("No active farm.")}, status=400)

        try:
            member = TeamMember.objects.get(user=user, farm=farm)
        except TeamMember.DoesNotExist:
            return Response({"detail": _("Not a member of this farm.")}, status=403)

        if member.expires_at and timezone.now() > member.expires_at:
            return Response({"detail": _("Access expired.")}, status=403)

        if not member.role:
            return Response([], status=200)

        permissions = member.role.permissions.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
