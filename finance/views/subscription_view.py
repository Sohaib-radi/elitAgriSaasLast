from finance.models.subscription import Subscription
from finance.serializers.subscription_serializer import SubscriptionSerializer
from core.viewsets.base import AutoPermissionViewSet

class SubscriptionViewSet(AutoPermissionViewSet):
    """
    🔁 Manage Subscriptions (e.g. internet, electricity, etc.)
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_module = "subscriptions"

    def get_queryset(self):
        return self.queryset.filter(farm=self.request.user.active_farm)
