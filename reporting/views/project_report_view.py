from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

from reporting.reports.project_report import ProjectReport
from reporting.services.report_service import ReportService

class ProjectReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filters = request.data
        user = request.user

        report = ProjectReport(filters=filters, user=user)
        pdf = ReportService.run(report, save_record=True)

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=project_report.pdf"
        return response
