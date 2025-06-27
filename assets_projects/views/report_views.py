from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..services.reporting_service import ReportingService

class ProjectCostReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        report = ReportingService.generate_cost_report(project_id)
        if report:
            return Response(report)
        return Response(
            {'detail': 'Project not found'},
            status=status.HTTP_404_NOT_FOUND
        )