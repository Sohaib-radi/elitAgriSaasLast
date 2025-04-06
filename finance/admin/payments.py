from django.contrib import admin
from finance.models.payment import Payment
from finance.models.receipt import Receipt
from finance.models.receipt_attachment import ReceiptAttachment

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("receipt_number", "person", "amount", "date", "farm")
    search_fields = ("receipt_number", "person__name")
    list_filter = ("date", "person__type")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("payment_number", "person", "amount", "date", "farm")
    search_fields = ("payment_number", "person__name")
    list_filter = ("date", "person__type")


@admin.register(ReceiptAttachment)
class ReceiptAttachmentAdmin(admin.ModelAdmin):
    list_display = ("receipt", "file", "uploaded_at")