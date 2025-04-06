from django.contrib import admin
from finance.models.expense_category import ExpenseCategory
from finance.models.expense_item import ExpenseItem


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "monthly_budget", "farm", "created_at")
    list_filter = ("type", "farm")
    search_fields = ("name", "code")


@admin.register(ExpenseItem)
class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = ("label", "amount", "category", "status", "date")
    list_filter = ("status", "date", "category__type")
    search_fields = ("label", "code", "description")
