from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from reporting.reports.receipt_report import ReceiptReport
from reporting.services.report_service import ReportService


class ReceiptReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filters = request.data
        user = request.user

        report = ReceiptReport(filters=filters, user=user)
        pdf = ReportService.run(report, save_record=True)

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=receipt_{}.pdf".format(filters.get("receipt_id", "voucher"))
        return response