from django.urls import path
from rest_framework.routers import DefaultRouter
from finance.views.payments import PaymentViewSet, ReceiptViewSet
from finance.views.payment_attachment import PaymentAttachmentUploadView
from finance.views.receipt_attachment import ReceiptAttachmentUploadView


router = DefaultRouter()
router.register("receipts", ReceiptViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = router.urls + [
    path("payments/<int:pk>/upload-attachments/", PaymentAttachmentUploadView.as_view(), name="payment-upload-attachments"),
    path("receipts/<int:pk>/upload-attachments/", ReceiptAttachmentUploadView.as_view(), name="receipt-upload-attachments"),
]
