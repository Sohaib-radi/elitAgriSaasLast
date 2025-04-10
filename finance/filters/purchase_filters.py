import django_filters
from finance.models.purchase import PurchaseInvoice
from finance.models.purchase import PurchasePayment


class PurchaseInvoiceFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="delivery_date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="delivery_date", lookup_expr="lte")
    supplier = django_filters.NumberFilter(field_name="supplier_id")
    total_min = django_filters.NumberFilter(field_name="total_amount", lookup_expr="gte")
    total_max = django_filters.NumberFilter(field_name="total_amount", lookup_expr="lte")

    class Meta:
        model = PurchaseInvoice
        fields = ["supplier", "payment_method"]


class PurchasePaymentFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    invoice = django_filters.NumberFilter(field_name="invoice_id")

    class Meta:
        model = PurchasePayment
        fields = ["invoice"]
