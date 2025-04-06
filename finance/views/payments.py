from core.viewsets.base import AutoPermissionViewSet

from finance.models.payment import Payment
from finance.models.receipt import Receipt
from finance.serializers.payments import PaymentSerializer, ReceiptSerializer


class ReceiptViewSet(AutoPermissionViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_module = "payments"

    def get_queryset(self):
        return super().get_queryset().filter(farm=self.request.user.active_farm)


class PaymentViewSet(AutoPermissionViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_module = "payments"

    def get_queryset(self):
        return super().get_queryset().filter(farm=self.request.user.active_farm)
