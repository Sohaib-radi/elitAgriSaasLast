from rest_framework import serializers
from farm_settings.models import FarmSettings




class FarmSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(write_only=True, required=False)
    logo_url = serializers.ImageField(source='farm.logo', read_only=True)
    slug = serializers.SlugField(source='farm.slug', read_only=True)

    class Meta:
        model = FarmSettings
        fields = [
                "id", "logo", "logo_url", "slug",
                "legal_name", "contact_person", "email", "telephone", "whatsapp_number",
                "website", "location_country", "region", "city", "address", "postal_code",
                "latitude", "longitude", "business_id", "tax_id", "license_number", "description",
                "start_date", "default_language", "currency", "currency_exchange_rate",
                "exchange_rate_updated_at",
                "allow_invites", "auto_activate_users", "role_mode",
                "enable_email_notifications", "low_stock_threshold", "daily_reminder_time",
                "print_template", "enable_barcode_printing", "report_format",
                "ai_enabled", "ai_tasks_enabled", "voice_commands",
                "session_expiry_minutes", "otp_enabled", "guest_mode_duration",
                "multi_farm_enabled", "auto_numbering_enabled", "attachment_required",
                "created_at", "updated_at"
            ]
        read_only_fields = ["id", "slug", "logo_url", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        logo = validated_data.pop('logo', None)
        instance = super().update(instance, validated_data)

        if logo:
            instance.farm.logo = logo
            instance.farm.save()

        return instance
