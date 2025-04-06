from django.urls import path
from rest_framework.routers import DefaultRouter
from finance.views.expense import ExpenseCategoryViewSet, ExpenseItemViewSet
from finance.views.expense_attachment import ExpenseItemAttachmentUploadView

router = DefaultRouter()
router.register("categories", ExpenseCategoryViewSet, basename="expense-category")
router.register("items", ExpenseItemViewSet, basename="expense-item")

urlpatterns = router.urls + [
    path("items/<int:pk>/upload-attachments/", ExpenseItemAttachmentUploadView.as_view(), name="expense-item-upload-attachments"),
]
