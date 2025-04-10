from rest_framework.parsers import MultiPartParser, FormParser
from core.viewsets.base import AutoPermissionViewSet
from finance.filters.purchase_filters import PurchaseInvoiceFilter, PurchasePaymentFilter
from finance.models.purchase import PurchaseInvoice, PurchasePayment, PurchaseAttachment
from django_filters.rest_framework import DjangoFilterBackend
from finance.serializers.purchase import (
    PurchaseInvoiceSerializer,
    PurchasePaymentSerializer,
    PurchaseAttachmentSerializer
)


class PurchaseInvoiceViewSet(AutoPermissionViewSet):
    queryset = PurchaseInvoice.objects.all()
    serializer_class = PurchaseInvoiceSerializer
    permission_module = "purchases"
    filterset_class = PurchaseInvoiceFilter
    filter_backends = [DjangoFilterBackend]
    def get_queryset(self):
        return self.queryset.filter(farm=self.request.user.active_farm)


class PurchasePaymentViewSet(AutoPermissionViewSet):
    queryset = PurchasePayment.objects.all()
    serializer_class = PurchasePaymentSerializer
    permission_module = "purchases"
    filterset_class = PurchasePaymentFilter
    filter_backends = [DjangoFilterBackend]
    def get_queryset(self):
        return self.queryset.filter(invoice__farm=self.request.user.active_farm)


class PurchaseAttachmentViewSet(AutoPermissionViewSet):
    queryset = PurchaseAttachment.objects.all()
    serializer_class = PurchaseAttachmentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_module = "purchases"


    def get_queryset(self):
        return self.queryset.filter(invoice__farm=self.request.user.active_farm)
