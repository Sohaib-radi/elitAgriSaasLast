from rest_framework import serializers
from core.models.person import Person
from product_catalogue.models.supplier import Supplier
from core.models.team import TeamMember


class PersonSerializer(serializers.ModelSerializer):
    supplier_id = serializers.PrimaryKeyRelatedField(
        source="supplier", queryset=Supplier.objects.all(), required=False, allow_null=True
    )
    team_member_id = serializers.PrimaryKeyRelatedField(
        source="team_member", queryset=TeamMember.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Person
        fields = [
            "id",
            "name",
            "phone",
            "address",
            "supplier_id",
            "team_member_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
