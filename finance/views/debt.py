from core.viewsets.base import AutoPermissionViewSet
from finance.models.debt import Debt
from finance.serializers.debt import DebtSerializer
from finance.filters.debt_filter import DebtFilter


class DebtViewSet(AutoPermissionViewSet):
    """
    Manage all debts (linked to people)
    """
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_module = "debts"
    filterset_class = DebtFilter

    def get_queryset(self):
        return self.queryset.filter(farm=self.request.user.active_farm)
