from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, permissions
from finance.models.payment import Payment
from finance.models.payment_attachment import PaymentAttachment
from finance.serializers.payments import PaymentAttachmentSerializer


class PaymentAttachmentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk, farm=request.user.active_farm)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=404)

        files = request.FILES.getlist("files")
        attachments = []

        for f in files:
            attachment = PaymentAttachment.objects.create(payment=payment, file=f)
            attachments.append(attachment)

        serializer = PaymentAttachmentSerializer(attachments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
