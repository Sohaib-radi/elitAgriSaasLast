import django_filters
from finance.models.receipt import Receipt


class ReceiptFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    person_id = django_filters.NumberFilter(field_name="person__id")

    class Meta:
        model = Receipt
        fields = ["start_date", "end_date", "person_id"]
