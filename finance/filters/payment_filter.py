import django_filters
from finance.models.payment import Payment


class PaymentFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    person_id = django_filters.NumberFilter(field_name="person__id")

    class Meta:
        model = Payment
        fields = ["start_date", "end_date", "person_id"]
