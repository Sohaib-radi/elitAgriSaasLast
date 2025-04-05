from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models.role import Role
from core.permissions.permissions import IsNotExpired
from core.serializers.role import RoleSerializer
from core.viewsets.base import AutoPermissionAPIView 


# TODO : MUST UPDATE TEH PERMISTION TO GENEREQUE PERMISION 


class RoleListView(AutoPermissionAPIView):
    permission_module = "roles" 

    def get(self, request):
        roles = Role.objects.all().order_by('name')
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)