from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta

import django_filters

from animal.models.vaccine import AnimalVaccine, VaccineStatus

class AnimalVaccineFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name="date_given", lookup_expr="gte")
    max_date = django_filters.DateFilter(field_name="date_given", lookup_expr="lte")
    status = django_filters.ChoiceFilter(choices=VaccineStatus.choices)
    name = django_filters.CharFilter(lookup_expr="icontains")

    expired = django_filters.BooleanFilter(method="filter_expired")
    soon_expire = django_filters.BooleanFilter(method="filter_soon_expire")

    def filter_expired(self, queryset, name, value):
        today = timezone.now().date()
        if value:
            return queryset.filter(valid_until__lt=today)
        return queryset

    def filter_soon_expire(self, queryset, name, value):
        today = timezone.now().date()
        if value:
            upcoming = today + timedelta(days=15)
            return queryset.filter(valid_until__gte=today, valid_until__lte=upcoming)
        return queryset

    class Meta:
        model = AnimalVaccine
        fields = [
            "animal", "status", "name",
            "min_date", "max_date",
            "expired", "soon_expire",
        ]
