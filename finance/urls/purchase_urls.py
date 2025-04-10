from rest_framework.routers import DefaultRouter
from finance.views.purchase import (
    PurchaseInvoiceViewSet,
    PurchasePaymentViewSet,
    PurchaseAttachmentViewSet
)

router = DefaultRouter()
router.register("invoices", PurchaseInvoiceViewSet, basename="purchase-invoice")
router.register("payments", PurchasePaymentViewSet, basename="purchase-payment")
router.register("attachments", PurchaseAttachmentViewSet, basename="purchase-attachment")

urlpatterns = router.urls
