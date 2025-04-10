from core.viewsets.base import AutoPermissionViewSet

from finance.models.payment import Payment
from finance.models.receipt import Receipt
from finance.serializers.payments import PaymentSerializer, ReceiptSerializer
from finance.filters.payment_filter import PaymentFilter
from django_filters.rest_framework import DjangoFilterBackend
from finance.filters.receipt_filter import ReceiptFilter

class ReceiptViewSet(AutoPermissionViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_module = "receipts"
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReceiptFilter
    
    def get_queryset(self):
        return super().get_queryset().filter(farm=self.request.user.active_farm)


class PaymentViewSet(AutoPermissionViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_module = "payments"
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    def get_queryset(self):
        return super().get_queryset().filter(farm=self.request.user.active_farm)
