from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

from reporting.reports.project_detail_report import ProjectDetailReport
from reporting.services.report_service import ReportService


class ProjectDetailReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filters = request.data
        user = request.user

        if "project_id" not in filters:
            return HttpResponse("Missing 'project_id' in filters", status=400)

        report = ProjectDetailReport(filters=filters, user=user)
        pdf = ReportService.run(report, save_record=True)

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=project_detail_report.pdf"
        return response
