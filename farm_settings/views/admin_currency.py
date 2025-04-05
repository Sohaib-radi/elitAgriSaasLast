

from rest_framework import viewsets
from farm_settings.models import Currency
from farm_settings.serializers.currency import CurrencySerializer
from rest_framework.permissions import IsAdminUser

class CurrencyAdminViewSet(viewsets.ModelViewSet):
    """
    Admin-only endpoint to manage global currencies (USD, EUR, etc.)
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAdminUser]
