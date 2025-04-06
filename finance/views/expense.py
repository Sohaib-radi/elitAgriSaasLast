from core.viewsets.base import AutoPermissionViewSet
from finance.models.expense_category import ExpenseCategory
from finance.models.expense_item import ExpenseItem
from finance.serializers.expense import ExpenseCategorySerializer, ExpenseItemSerializer


class ExpenseCategoryViewSet(AutoPermissionViewSet):
    """
    Manage Expense Categories (lists)
    """
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_module = "expenses"
   

    def get_queryset(self):
        return self.queryset.filter(farm=self.request.user.active_farm)


class ExpenseItemViewSet(AutoPermissionViewSet):
    """
    Manage individual expenses inside a category
    """
    queryset = ExpenseItem.objects.all()
    serializer_class = ExpenseItemSerializer
    permission_module = "expenses"
    def get_queryset(self):
        return self.queryset.filter(farm=self.request.user.active_farm)
