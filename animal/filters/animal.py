import django_filters
from animal.models.animal import Animal


class AnimalFilter(django_filters.FilterSet):
    birth_date__gte = django_filters.DateFilter(field_name="birth_date", lookup_expr="gte")
    birth_date__lte = django_filters.DateFilter(field_name="birth_date", lookup_expr="lte")

    class Meta:
        model = Animal
        fields = {
            "species": ["exact"],
            "gender": ["exact"],
            "status": ["exact"],
            "list": ["exact"],
        }
