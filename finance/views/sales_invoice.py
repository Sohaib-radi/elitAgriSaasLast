from core.viewsets.base import AutoPermissionViewSet
from finance.models.sales_invoice import SalesInvoice
from finance.serializers.sales_invoice import SalesInvoiceSerializer
from finance.filters.sales_invoice_filters import SalesInvoiceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class SalesInvoiceViewSet(AutoPermissionViewSet):
    """
    Viewset for managing sales invoices with multi-item support,
    respecting Elite Agri structure and permissions.
    """
    queryset = SalesInvoice.objects.all()
    serializer_class = SalesInvoiceSerializer
    permission_required = "finance.manage_sales"
    permission_module = "invoices"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SalesInvoiceFilter
    search_fields = ["invoice_number", "buyer__name"]
    ordering_fields = ["date", "total_amount", "created_at"]

    def get_queryset(self):
        return self.queryset.filter(
            farm=self.request.user.active_farm
        ).select_related("buyer").prefetch_related("items")
