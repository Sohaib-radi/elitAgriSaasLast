import os
import datetime
import json
from collections import defaultdict
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.utils.functional import Promise
from finance.models.expense_item import ExpenseItem
from finance.models.expense_category import ExpenseCategory
from reporting.base.base import BaseReport
from reporting.utils.render_pdf import render_to_pdf
from reporting.utils.save_report_record import save_report_record
from reporting.utils.plotly_helpers import generate_expense_chart, generate_grouped_expense_chart



class ExpenseReport(BaseReport):
    """
    Professional expense report with filtering, summaries, and chart-ready data.
    """

    def make_serializable_filters(self):
        cleaned = {}
        for k, v in self.filters.items():
            if hasattr(v, "pk"):
                cleaned[k] = v.pk
            elif isinstance(v, list):
                cleaned[k] = [item.pk if hasattr(item, "pk") else str(item) for item in v]
            elif isinstance(v, (datetime.datetime, datetime.date)):
                cleaned[k] = v.isoformat()
            elif isinstance(v, Promise):  # gettext_lazy, __proxy__
                cleaned[k] = str(v)
            else:
                try:
                    cleaned[k] = str(v)
                except Exception:
                    cleaned[k] = None
        return cleaned

    def fetch(self):
        queryset = ExpenseItem.objects.filter(farm=self.user.active_farm)

        start = self.filters.get("start")
        end = self.filters.get("end")
        category_id = self.filters.get("category_id")
        status = self.filters.get("status")

        if start and end:
            queryset = queryset.filter(date__range=[start, end])
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if status:
            queryset = queryset.filter(status=status)

        queryset = queryset.select_related("category")
        return queryset

    def format(self, data):
        expense_rows = []
        total_amount = 0
        type_totals = defaultdict(float)
        monthly_by_type = defaultdict(lambda: defaultdict(float))  # {month -> {type -> amount}}

        for expense in data:
            category = expense.category
            amount = float(expense.amount)
            total_amount += amount

            type_label = str(category.get_type_display())
            type_totals[category.type] += amount

            month_label = expense.date.strftime('%b %Y')  # e.g., "Jul 2025"
            monthly_by_type[month_label][type_label] += amount

            expense_rows.append({
                "date": expense.date.strftime("%Y-%m-%d"),
                "label": expense.label,
                "amount": amount,
                "category": category.name,
                "type": type_label,
                "status": str(expense.get_status_display()),
            })

        # 🔢 Top expense type
        top_type = max(type_totals.items(), key=lambda x: x[1], default=(None, 0))
        top_type_name = str(ExpenseCategory.CategoryType(top_type[0]).label) if top_type[0] else "—"
        top_type_amount = round(top_type[1], 2)
        top_expense_item = max(data, key=lambda e: e.amount, default=None)
        if top_expense_item:
            top_expense_display = f"{top_expense_item.label} - ${top_expense_item.amount:.2f}"
        else:
            top_expense_display = "—"

        # 📊 Pie chart data
        chart_data = [
            {"label": str(ExpenseCategory.CategoryType(t).label), "amount": round(amt, 2)}
            for t, amt in type_totals.items()
        ]
        chart_image_path = None
        relative_chart_path = None
        if chart_data:
            chart_image_path = generate_expense_chart(chart_data)
            relative_chart_path = str(chart_image_path).replace(str(settings.MEDIA_ROOT), settings.MEDIA_URL)

        # 📊 Grouped bar chart data (Monthly x Expense Type)
        all_months = sorted(monthly_by_type.keys())
        all_types = sorted({etype for month_data in monthly_by_type.values() for etype in month_data})
        grouped_data = {
            etype: [monthly_by_type[month].get(etype, 0) for month in all_months]
            for etype in all_types
        }

        monthly_grouped_chart = generate_grouped_expense_chart(all_months, grouped_data)
        
        # 🧪 Clean filters (for DB/logging)
        serialized_filters = self.make_serializable_filters()

        # 🕒 Report timestamp (string format for PDF-safe rendering)
        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        # 📄 Final context
        context = self.get_context()
        context.update({
            "expenses": expense_rows,
            "total_amount": round(total_amount, 2),
            "top_type_name": top_type_name,
            "top_type_amount": top_type_amount,
            "chart_data": chart_data,
            "chart_image_path": relative_chart_path,
            "monthly_grouped_chart": monthly_grouped_chart,
            
            "filters": serialized_filters,
            "farm": self.user.active_farm,
            "generated_by": self.user.get_full_name(),
            "now": now,
             "summary_cards": [
                 {"title": "Total Expenses", "description": f"${total_amount}"},
                 {"title": "Top Category", "description": f"{top_type_name}: {top_type_amount}"},
                 {"title": "Top Expense", "description": top_expense_display},
             ]
        })
        # 📦 Render and generate PDF
        pdf = self.render_pdf("reports/expense_report.html", context)

        # 🧹 Cleanup temp chart image
        try:
            if chart_image_path and os.path.exists(chart_image_path):
                os.remove(chart_image_path)
        except Exception as e:
            print(f"[WARN] Failed to delete temp chart image: {e}")

        return pdf
