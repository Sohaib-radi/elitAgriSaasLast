from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from reporting.reports.financial_summary_comparison_report import FinancialSummaryComparisonReport
from reporting.services.report_service import ReportService


class FinancialSummaryReportView(APIView):
    """
    API endpoint for generating financial summary comparison report (income vs expenses).
    Accepts two date ranges (start1/end1 and start2/end2).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filters = request.data
        user = request.user

        report = FinancialSummaryComparisonReport(filters=filters, user=user)
        pdf = ReportService.run(report, save_record=True)

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=financial_summary_comparison.pdf"
        return response
