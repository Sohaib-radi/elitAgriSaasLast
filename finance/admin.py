from django.contrib import admin

from finance.models.expense_category import ExpenseCategory
from finance.models.expense_item import ExpenseItem
from finance.models.payment import Payment
from finance.models.expense_item_attachment import ExpenseItemAttachment
from finance.models.receipt import Receipt
from finance.models.receipt_attachment import ReceiptAttachment
from finance.models.payment_attachment import PaymentAttachment
from finance.models.buyer import Buyer
from finance.models.debt import Debt
from finance.models.purchase import PurchaseInvoice
from finance.models.sales_invoice import SalesInvoice, SalesInvoiceItem
from finance.models.subscription import Subscription
from finance.models.service_company import ServiceCompany

def all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = all_fields(ExpenseCategory)

@admin.register(ExpenseItem)
class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = all_fields(ExpenseItem)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = all_fields(Payment)

@admin.register(ExpenseItemAttachment)
class ExpenseItemAttachmentAdmin(admin.ModelAdmin):
    list_display = all_fields(ExpenseItemAttachment)

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = all_fields(Receipt)

@admin.register(ReceiptAttachment)
class ReceiptAttachmentAdmin(admin.ModelAdmin):
    list_display = all_fields(ReceiptAttachment)

@admin.register(PaymentAttachment)
class PaymentAttachmentAdmin(admin.ModelAdmin):
    list_display = all_fields(PaymentAttachment)

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = all_fields(Buyer)

@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = all_fields(Debt)

@admin.register(PurchaseInvoice)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = all_fields(PurchaseInvoice)

class SalesInvoiceItemInline(admin.TabularInline):
    model = SalesInvoiceItem
    extra = 0
    readonly_fields = ("total",)

@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id", "invoice_number", "buyer", "status",
        "date", "delivery_date",
        "subtotal", "discount", "shipping", "taxes", "vat", "total_amount",
        "payment_method",
        "created_at", "updated_at",
    )
    list_filter = ("status", "payment_method", "date", "delivery_date")
    search_fields = ("invoice_number", "buyer__name")
    inlines = [SalesInvoiceItemInline]
    readonly_fields = ("subtotal", "total_amount", "created_at", "updated_at")
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_totals()

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = all_fields(Subscription)

@admin.register(ServiceCompany)
class ServiceCompanyAdmin(admin.ModelAdmin):
    list_display = all_fields(ServiceCompany)
