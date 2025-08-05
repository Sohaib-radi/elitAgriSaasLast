from collections import defaultdict
from decimal import Decimal, InvalidOperation
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from reporting.base.base import BaseReport
from reporting.utils.save_report_record import save_report_record
from finance.models.receipt import Receipt
from finance.models.payment import Payment
from django.utils.functional import Promise
import datetime

class FinancialSummaryComparisonReport(BaseReport):
    """
    💼 Full financial summary comparing income and expenses across two periods.
    Designed for executive-level decision making.
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
        today = timezone.now().date()

        # Get filters
        start1 = self.filters.get("start1")
        end1 = self.filters.get("end1")
        start2 = self.filters.get("start2")
        end2 = self.filters.get("end2")

        # Default: compare last 30 days vs previous 30 days
        if not any([start1, end1, start2, end2]):
            end1 = today
            start1 = end1 - timedelta(days=30)
            end2 = start1 - timedelta(days=1)
            start2 = end2 - timedelta(days=30)

        # Fill missing pairs
        if start1 and not end1:
            end1 = today
        if end1 and not start1:
            start1 = end1 - timedelta(days=30)

        if start2 and not end2:
            end2 = today
        if end2 and not start2:
            start2 = end2 - timedelta(days=30)

        # Load receipts/payments for both periods
        data = {}

        if start1 and end1:
            data["period_1"] = {
                "start": start1,
                "end": end1,
                "receipts": Receipt.objects.filter(
                    farm=self.user.active_farm,
                    date__range=[start1, end1]
                ).select_related("person"),
                "payments": Payment.objects.filter(
                    farm=self.user.active_farm,
                    date__range=[start1, end1]
                ).select_related("person"),
            }

        if start2 and end2:
            data["period_2"] = {
                "start": start2,
                "end": end2,
                "receipts": Receipt.objects.filter(
                    farm=self.user.active_farm,
                    date__range=[start2, end2]
                ).select_related("person"),
                "payments": Payment.objects.filter(
                    farm=self.user.active_farm,
                    date__range=[start2, end2]
                ).select_related("person"),
            }

        return data

    def format(self, data):
        def summarize(receipts, payments, label, start, end):
            income = sum([r.amount for r in receipts])
            expense = sum([p.amount for p in payments])
            net_profit = income - expense
            profit_margin = f"{(net_profit / income * 100):.1f}%" if income > 0 else "0%"

            top_payers = defaultdict(Decimal)
            for r in receipts:
                top_payers[r.person.name] += r.amount
            top_payers = sorted(top_payers.items(), key=lambda x: x[1], reverse=True)[:5]

            top_expenses = defaultdict(Decimal)
            for p in payments:
                top_expenses[p.person.name] += p.amount
            top_expenses = sorted(top_expenses.items(), key=lambda x: x[1], reverse=True)[:5]

            return {
                "label": label,
                "start": start,
                "end": end,
                "total_income": round(income, 2),
                "total_expenses": round(expense, 2),
                "net_profit": round(net_profit, 2),
                "profit_margin": profit_margin,
                "top_payers": [(k, f"${v:,.2f}") for k, v in top_payers],
                "top_expenses": [(k, f"${v:,.2f}") for k, v in top_expenses],
            }

        context = self.get_context()
        now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        context.update({
            "now": now,
            "farm": self.user.active_farm,
            "user": self.user.get_full_name(),
        })

        period_1 = period_2 = None
        if "period_1" in data:
            p1 = data["period_1"]
            period_1 = summarize(p1["receipts"], p1["payments"], "Period 1", p1["start"], p1["end"])
            context["period_1"] = period_1

        if "period_2" in data:
            p2 = data["period_2"]
            period_2 = summarize(p2["receipts"], p2["payments"], "Period 2", p2["start"], p2["end"])
            context["period_2"] = period_2

        # Build comparison analysis
        if period_1 and period_2:
            def format_delta(val1, val2):
                try:
                    val1 = Decimal(val1)
                    val2 = Decimal(val2)
                    change = val2 - val1
                    pct = (change / val1 * 100) if val1 else 0
                    return f"{'+' if change >= 0 else ''}${abs(change):,.0f}", f"{pct:+.1f}%", "positive" if change >= 0 else "negative"
                except InvalidOperation:
                    return "-", "-", "neutral"

            comparison = []

            metrics = [
                ("Total Income", period_1["total_income"], period_2["total_income"]),
                ("Total Expenses", period_1["total_expenses"], period_2["total_expenses"]),
                ("Net Profit", period_1["net_profit"], period_2["net_profit"]),
                ("Profit Margin", period_1["profit_margin"].replace('%', ''), period_2["profit_margin"].replace('%', '')),
            ]

            for label, val1, val2 in metrics:
                change, pct, typ = format_delta(val1, val2)
                comparison.append({
                    "metric": label,
                    "period_1": f"${val1:,.0f}" if "Profit Margin" not in label else f"{val1}%",
                    "period_2": f"${val2:,.0f}" if "Profit Margin" not in label else f"{val2}%",
                    "change": change,
                    "percent_change": pct,
                    "change_type": typ,
                })

            # Top expense comparison
            top1 = period_1["top_expenses"][0] if period_1["top_expenses"] else ("N/A", "$0")
            top2 = period_2["top_expenses"][0] if period_2["top_expenses"] else ("N/A", "$0")
            top1_val = Decimal(top1[1].replace("$", "").replace(",", ""))
            top2_val = Decimal(top2[1].replace("$", "").replace(",", ""))
            change, pct, typ = format_delta(top1_val, top2_val)
            comparison.append({
                "metric": "Top Expense",
                "period_1": f"{top1[0]}<br>{top1[1]}",
                "period_2": f"{top2[0]}<br>{top2[1]}",
                "change": change,
                "percent_change": pct,
                "change_type": typ,
            })

            context["comparison"] = comparison

        # PDF generation (optional)
        pdf_content = self.render_pdf("reports/financial_summary_comparison.html", context)

        # Save record
        save_report_record(
            user=self.user,
            report_type="financial_summary",
            report_name="Financial Summary Comparison",
            pdf_content=pdf_content,
            filters=self.make_serializable_filters(),
        )

        return pdf_content
