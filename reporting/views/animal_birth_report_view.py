# reporting/views/animal_birth_report_view.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

from reporting.reports.animal_birth_report import AnimalBirthReport
from reporting.services.report_service import ReportService

class AnimalBirthReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        filters = request.data
        user = request.user

        report = AnimalBirthReport(filters=filters, user=user)
        pdf = ReportService.run(report, save_record=True)

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=animal_birth_report.pdf"
        return response
