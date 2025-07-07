from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, permissions
from finance.models.debt import Debt
from finance.models.debt import DebtAttachment
from finance.serializers.debt import DebtAttachmentSerializer


class DeptItemAttachmentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            expense_item = Debt.objects.get(pk=pk, farm=request.user.active_farm)
        except Debt.DoesNotExist:
            return Response({"detail": "Expense item not found."}, status=404)

        files = request.FILES.getlist("files")  # 👈 Send `files[]` from frontend
        attachments = []

        for f in files:
            attachment = Debt.objects.create(expense_item=expense_item, file=f)
            attachments.append(attachment)

        serializer = DebtAttachmentSerializer(attachments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)