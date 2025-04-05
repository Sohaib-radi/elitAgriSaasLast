import django_filters
from animal.models.field import CustomListField


class CustomListFieldFilter(django_filters.FilterSet):
    class Meta:
        model = CustomListField
        fields = ["list","required"]  
