from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import Farm

class FarmSettings(models.Model):
    """
    🔧 FarmSettings is a one-to-one configuration model linked to each Farm.
    It holds language, currency, features toggles, security, and operational settings.
    """
    farm = models.OneToOneField(Farm, on_delete=models.CASCADE, related_name="settings", verbose_name=_("Farm"))

    # 🌍 General Info
    legal_name = models.CharField(max_length=255, verbose_name=_("Legal Name"), help_text=_("The official registered name of the farm/company."), blank=True, null=True)
    contact_person = models.CharField(max_length=100, verbose_name=_("Contact Person"), help_text=_("Primary contact for the farm (e.g., owner or manager)."), blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"), help_text=_("Official email address for the farm."))
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Telephone"), help_text=_("Primary contact number."))
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("WhatsApp Number"), help_text=_("WhatsApp contact for quick communication."))
    website = models.URLField(blank=True, null=True, verbose_name=_("Website"), help_text=_("Farm or company website."))
    location_country = models.CharField(max_length=100, verbose_name=_("Country"), blank=True, null=True, help_text=_("Country where the farm is located."))
    region = models.CharField(max_length=100, verbose_name=_("Region"), blank=True, null=True, help_text=_("Administrative region or province."))
    city = models.CharField(max_length=100, verbose_name=_("City"), blank=True, null=True)
    address = models.TextField(verbose_name=_("Address"), blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Postal Code"))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_("Latitude"), help_text=_("Latitude for mapping and delivery."))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_("Longitude"), help_text=_("Longitude for mapping and delivery."))
    business_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Business ID"), help_text=_("Tax registration number or SIRET."))
    tax_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Tax ID"), help_text=_("VAT or fiscal identification number."))
    license_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("License Number"), help_text=_("Authorization/license number if applicable."))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True, help_text=_("Short bio or summary about the farm."))
    start_date = models.DateField(verbose_name=_("Start Date"), blank=True, null=True, help_text=_("Date the farm was established."))

    # 🌐 Language & Currency
    default_language = models.CharField(max_length=10, choices=[('en', 'English'), ('ar', 'Arabic'), ('fr', 'French'), ('tr', 'Turkish')], default='en', verbose_name=_("Default Language"))
    currency = models.CharField(max_length=10, default='USD', verbose_name=_("Currency"))
    currency_exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1.0, verbose_name=_("Exchange Rate"))
    exchange_rate_updated_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Last Exchange Rate Update"))

    # 👥 User Management
    allow_invites = models.BooleanField(default=True, verbose_name=_("Allow User Invitations"), help_text=_("Enable or disable inviting new users to the farm."))
    auto_activate_users = models.BooleanField(default=False, verbose_name=_("Auto-activate New Users"), help_text=_("If true, users are active immediately after being invited or registering."))
    role_mode = models.CharField(max_length=20, choices=[('simple', 'Simple'), ('advanced', 'Advanced')], default='advanced', verbose_name=_("Role Mode"), help_text=_("Simple: fixed roles. Advanced: granular permissions."))

    # 🔔 Notifications
    enable_email_notifications = models.BooleanField(default=True, verbose_name=_("Enable Email Notifications"))
    low_stock_threshold = models.PositiveIntegerField(default=10, verbose_name=_("Low Stock Alert Threshold"))
    daily_reminder_time = models.TimeField(blank=True, null=True, verbose_name=_("Daily Reminder Time"))

    # 📊 Reports & Printing
    print_template = models.CharField(max_length=50, default='default', verbose_name=_("Print Template"))
    enable_barcode_printing = models.BooleanField(default=False, verbose_name=_("Enable Barcode Printing"))
    report_format = models.CharField(max_length=20, choices=[('summary', 'Summary'), ('detailed', 'Detailed')], default='summary', verbose_name=_("Report Format"))

    # 🤖 Smart Features
    ai_enabled = models.BooleanField(default=False, verbose_name=_("Enable AI Assistance"), help_text=_("Enable AI-based suggestions and task automation."))
    ai_tasks_enabled = models.JSONField(blank=True, null=True, verbose_name=_("AI Tasks Enabled"), help_text=_("List of AI-enabled tasks like reports or automation."))
    voice_commands = models.BooleanField(default=False, verbose_name=_("Enable Voice Commands"))

    # 🔐 Security
    session_expiry_minutes = models.IntegerField(default=120, verbose_name=_("Session Timeout (minutes)"))
    otp_enabled = models.BooleanField(default=False, verbose_name=_("Two-Factor Authentication (OTP)"))
    guest_mode_duration = models.IntegerField(default=60, verbose_name=_("Guest Mode Duration (minutes)"), help_text=_("Temporary access mode duration in minutes."))

    # ⚙️ Advanced
    multi_farm_enabled = models.BooleanField(default=True, verbose_name=_("Enable Multi-Farm Support"), help_text=_("Allows switching between farms (if authorized)."))
    auto_numbering_enabled = models.BooleanField(default=True, verbose_name=_("Enable Auto Numbering"), help_text=_("Automatically number transactions and forms."))
    attachment_required = models.BooleanField(default=False, verbose_name=_("Require Attachment on Forms"), help_text=_("Force users to attach documents for certain forms."))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"Settings for {self.farm.name}"

    @property
    def has_ai_features(self):
        return self.ai_enabled and bool(self.ai_tasks_enabled)

    # Utility accessors for logic in views or decorators
    def can_invite_users(self):
        return self.allow_invites

    def should_auto_activate_users(self):
        return self.auto_activate_users

    def is_guest_mode_active(self):
        return self.guest_mode_duration > 0

    def is_multi_farm_enabled(self):
        return self.multi_farm_enabled

    def is_auto_numbering_on(self):
        return self.auto_numbering_enabled

    def is_attachment_required(self):
        return self.attachment_required

    def is_ai_enabled(self):
        return self.ai_enabled

    def get_role_mode(self):
        return self.role_mode
