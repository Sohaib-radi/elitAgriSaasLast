import django_filters
from crop.models.land_status import LandStatus, LandStatusChoices
from crop.models.crop import Crop, CropStatusChoices, UsageChoices
from crop.models.agricultural_land import AgriculturalLand


class LandStatusFilter(django_filters.FilterSet):
    agricultural_land = django_filters.NumberFilter()
    status = django_filters.ChoiceFilter(choices=LandStatusChoices.choices)
    product_used = django_filters.NumberFilter()
    from_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    has_product = django_filters.BooleanFilter(method="filter_has_product")

    def filter_has_product(self, queryset, name, value):
        if value:
            return queryset.exclude(product_used__isnull=True)
        return queryset.filter(product_used__isnull=True)

    class Meta:
        model = LandStatus
        fields = []


class CropFilter(django_filters.FilterSet):
    agricultural_land = django_filters.NumberFilter()
    status = django_filters.MultipleChoiceFilter(choices=CropStatusChoices.choices)
    usage = django_filters.MultipleChoiceFilter(choices=UsageChoices.choices)
    from_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Crop
        fields = []


class AgriculturalLandFilter(django_filters.FilterSet):
    land = django_filters.NumberFilter()
    code = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = AgriculturalLand
        fields = []
