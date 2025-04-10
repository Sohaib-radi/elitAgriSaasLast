import django_filters
from finance.models.sales_invoice import SalesInvoice

class SalesInvoiceFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    buyer = django_filters.NumberFilter(field_name="buyer__id")
    payment_method = django_filters.CharFilter(field_name="payment_method", lookup_expr="iexact")
    invoice_number = django_filters.CharFilter(field_name="invoice_number", lookup_expr="icontains")

    class Meta:
        model = SalesInvoice
        fields = ["buyer", "payment_method", "start_date", "end_date", "invoice_number"]
