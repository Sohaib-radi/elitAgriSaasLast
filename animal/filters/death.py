import django_filters
from animal.models.death import AnimalDeath

class AnimalDeathFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name="datetime", lookup_expr="gte")
    max_date = django_filters.DateFilter(field_name="datetime", lookup_expr="lte")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    animal = django_filters.NumberFilter(field_name="animal_id")

    class Meta:
        model = AnimalDeath
        fields = ["status", "animal"]
