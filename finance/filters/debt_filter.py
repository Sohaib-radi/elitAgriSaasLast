import django_filters
from finance.models.debt import Debt




# ?person_id=
# ?status=
# ?min_amount=
# ?max_amount=
# ?due_before=
# ?due_after=


class DebtFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    due_before = django_filters.DateFilter(field_name="due_date", lookup_expr="lte")
    due_after = django_filters.DateFilter(field_name="due_date", lookup_expr="gte")
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    person_id = django_filters.NumberFilter(field_name="person__id")

    class Meta:
        model = Debt
        fields = ["status", "person_id", "due_date"]
