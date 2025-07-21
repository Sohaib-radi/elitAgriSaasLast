from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

from reporting.reports.animal_death import AnimalDeathReport
from reporting.services.report_service import ReportService


class AnimalDeathReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filters = request.data
        user = request.user

        report = AnimalDeathReport(filters=filters, user=user)

        pdf = ReportService.run(report, save_record=True)

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=animal_death_report.pdf"
        return response
