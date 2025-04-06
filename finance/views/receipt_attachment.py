from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, permissions
from finance.models.receipt import Receipt
from finance.models.receipt_attachment import ReceiptAttachment
from finance.serializers.payments import ReceiptAttachmentSerializer


class ReceiptAttachmentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            receipt = Receipt.objects.get(pk=pk, farm=request.user.active_farm)
        except Receipt.DoesNotExist:
            return Response({"detail": "Receipt not found."}, status=404)

        files = request.FILES.getlist("files")
        attachments = []

        for f in files:
            attachment = ReceiptAttachment.objects.create(receipt=receipt, file=f)
            attachments.append(attachment)

        serializer = ReceiptAttachmentSerializer(attachments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
