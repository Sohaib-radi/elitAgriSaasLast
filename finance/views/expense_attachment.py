from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, permissions
from finance.models.expense_item import ExpenseItem
from finance.models.expense_item_attachment import ExpenseItemAttachment
from finance.serializers.expense import ExpenseItemAttachmentSerializer


class ExpenseItemAttachmentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            expense_item = ExpenseItem.objects.get(pk=pk, farm=request.user.active_farm)
        except ExpenseItem.DoesNotExist:
            return Response({"detail": "Expense item not found."}, status=404)

        files = request.FILES.getlist("files")  # 👈 Send `files[]` from frontend
        attachments = []

        for f in files:
            attachment = ExpenseItemAttachment.objects.create(expense_item=expense_item, file=f)
            attachments.append(attachment)

        serializer = ExpenseItemAttachmentSerializer(attachments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
