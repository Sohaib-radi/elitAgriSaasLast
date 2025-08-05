from django.urls import path
from reporting.views.expense_report import ExpenseReportView
from reporting.views.financial_summary_report_view import FinancialSummaryReportView
from reporting.views.payment_report_view import PaymentReportView
from reporting.views.receipt_report_view import ReceiptReportView
from reporting.views.test import ExpenseReportHTMLPreviewView, my_html_view, test_expense_report_view

urlpatterns = [
    path("expenses/", ExpenseReportView.as_view(), name="expense-report"),
    path("receipt/", ReceiptReportView.as_view(), name="receipt-report"),
    path("payment/", PaymentReportView.as_view(), name="payment-report"),
    path("summary/", FinancialSummaryReportView.as_view(), name="summary-report"),
]
urlpatterns += [
    path("html-preview/", test_expense_report_view, name="expense-report-preview"),
    path("my-page/", my_html_view, name="my_html_page"),
]