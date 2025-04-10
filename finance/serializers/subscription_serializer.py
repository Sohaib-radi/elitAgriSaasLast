

from rest_framework import serializers
from finance.models.subscription import Subscription
from finance.models.service_company import ServiceCompany

class SubscriptionSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "id", "subscription_number", "name", "company", "company_name",
            "account_number", "monthly_fee", "payment_method",
            "start_date", "end_date", "description", "address", "image",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
