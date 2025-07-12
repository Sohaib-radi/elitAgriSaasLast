from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.db.models import Sum, Q
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

from banking.models.bank import Bank
from banking.models.bank_transaction import BankTransaction

class BankDashboardViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint returning all banks with detailed financial dashboard data.
    """

    queryset = Bank.objects.all().select_related("main_currency").order_by("name")
    permission_module = "banking"

    def list(self, request, *args, **kwargs):
        data = []
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)

        for bank in self.get_queryset():
            transactions = BankTransaction.objects.filter(bank=bank)

            income = transactions.filter(
                transaction_type__in=["deposit", "loan_disbursement", "interest"]
            ).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')

            expense = transactions.filter(
                transaction_type__in=["withdrawal", "loan_payment", "fee"]
            ).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')

            current_balance = income - expense

            # Balance statistics for last 30 days
            balance_stats = (
                transactions.filter(transaction_date__gte=last_30_days)
                .values("transaction_date")
                .annotate(
                    income=Sum("amount", filter=Q(transaction_type__in=["deposit", "loan_disbursement", "interest"])),
                    expense=Sum("amount", filter=Q(transaction_type__in=["withdrawal", "loan_payment", "fee"]))
                )
                .order_by("transaction_date")
            )

            # Expense categories
            expense_categories = (
                transactions.filter(transaction_type__in=["withdrawal", "loan_payment", "fee"])
                .values("transaction_type")
                .annotate(total=Sum("amount"))
                .order_by("-total")
            )

            # Recent transactions (last 5)
            recent_transactions = transactions.order_by("-transaction_date")[:5].values(
                "id", "transaction_date", "amount", "transaction_type", "payment_method", "reference", "status"
            )

            data.append({
                "bank_id": bank.id,
                "name": bank.name,
                "account_number": bank.account_number,
                "iban": bank.iban,
                "swift_code": bank.swift_code,
                "phone_number": bank.phone_number,
                "email": bank.email,
                "main_currency": bank.main_currency.code if bank.main_currency else None,
                "description": bank.description,
                "income": income,
                "expense": expense,
                "current_balance": current_balance,
                "balance_statistics": list(balance_stats),
                "expense_categories": list(expense_categories),
                "recent_transactions": list(recent_transactions),
            })

        return Response(data)
