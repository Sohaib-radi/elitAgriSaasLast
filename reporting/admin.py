# reporting/admin.py
from django.contrib import admin
from reporting.models.report import ReportRecord

@admin.register(ReportRecord)
class ReportRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "status", "created_by", "executed_at", "created_at")
    list_filter = ("status", "type", "created_at")
    search_fields = ("name", "type", "created_by__email")
    readonly_fields = ("created_at", "updated_at", "executed_at")
