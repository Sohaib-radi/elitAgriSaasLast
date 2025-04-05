# crop/serializers/statistics.py

from rest_framework import serializers

class CropStatisticsSerializer(serializers.Serializer):
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
    wilaya_id = serializers.IntegerField(required=False)
    usage = serializers.ChoiceField(
        choices=[("for_sale", "For Sale"), ("for_feed", "For Feed")],
        required=False
    )
