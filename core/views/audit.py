from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from core.models.audit import UserLog
from core.serializers.audit import UserLogSerializer

class UserLogListView(ListAPIView):
    queryset = UserLog.objects.select_related('user', 'farm')
    serializer_class = UserLogSerializer
    permission_classes = [IsAdminUser]
