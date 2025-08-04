from django.urls import path
from reporting.views.expense_report import ExpenseReportView
from reporting.views.test import ExpenseReportHTMLPreviewView, test_expense_report_view

urlpatterns = [
    path("expenses/", ExpenseReportView.as_view(), name="expense-report"),
]
urlpatterns += [
    path("html-preview/", test_expense_report_view, name="expense-report-preview"),
]