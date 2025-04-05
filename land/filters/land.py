import django_filters
from land.models.land import Land

class LandFilter(django_filters.FilterSet):
    min_area = django_filters.NumberFilter(field_name="area", lookup_expr="gte")
    max_area = django_filters.NumberFilter(field_name="area", lookup_expr="lte")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    wilaya = django_filters.NumberFilter(field_name="wilaya__id")
    land_type = django_filters.CharFilter(field_name="land_type")
    status = django_filters.CharFilter(field_name="status")
    international_number = django_filters.CharFilter(lookup_expr="icontains")
    land_number = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Land
        fields = [
            "wilaya", "land_type", "status", "international_number", "land_number",
        ]
