import django_filters
from animal.models.birth import AnimalBirth


class AnimalBirthFilter(django_filters.FilterSet):
    moved_to_animals = django_filters.BooleanFilter()
    min_birth_date = django_filters.DateFilter(field_name="birth_datetime", lookup_expr="gte")
    max_birth_date = django_filters.DateFilter(field_name="birth_datetime", lookup_expr="lte")

    class Meta:
        model = AnimalBirth
        fields = ["moved_to_animals", "mother", "father", "species"]
