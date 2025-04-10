from rest_framework.routers import DefaultRouter
from finance.views.sales_invoice import SalesInvoiceViewSet

router = DefaultRouter()
router.register("sales-invoices", SalesInvoiceViewSet, basename="sales-invoice")

urlpatterns = router.urls