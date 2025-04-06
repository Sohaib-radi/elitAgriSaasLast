from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from datetime import datetime
from farm_settings.models import Currency, FarmCurrency, CurrencyRate
from farm_settings.serializers.currency import (
    CurrencySerializer,
    FarmCurrencySerializer,
    CurrencyRateSerializer,
)
from core.permissions.permissions import IsFarmOwnerOrReadOnly
from django.utils.translation import gettext_lazy as _

class AvailableCurrencyListView(generics.ListAPIView):
    """
    Global ISO currencies available for selection
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]


class FarmCurrencyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing farm-specific currencies
    """
    serializer_class = FarmCurrencySerializer
    permission_classes = [IsAuthenticated, IsFarmOwnerOrReadOnly]

    def get_queryset(self):
        return FarmCurrency.objects.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(
            farm=self.request.user.active_farm,
            created_by=self.request.user
        )


class CurrencyRateView(generics.ListCreateAPIView):
    serializer_class = CurrencyRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        farm_currency = get_object_or_404(
            FarmCurrency, id=self.kwargs["pk"], farm=self.request.user.active_farm
        )
        return CurrencyRate.objects.filter(farm_currency=farm_currency)

    def create(self, request, *args, **kwargs):
        farm_currency = get_object_or_404(
            FarmCurrency, id=self.kwargs["pk"], farm=self.request.user.active_farm
        )

        data = request.data
        many = isinstance(data, list)

        # Inject farm_currency into input (not created_by — handled later)
        if many:
            for item in data:
                item["farm_currency"] = farm_currency.id
        else:
            data["farm_currency"] = farm_currency.id

        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)

        # Here we inject created_by properly
        instances = serializer.save()
        if many:
            for instance in instances:
                instance.created_by = request.user
                instance.save(update_fields=["created_by"])
        else:
            instances.created_by = request.user
            instances.save(update_fields=["created_by"])

        return Response(self.get_serializer(instances, many=many).data, status=status.HTTP_201_CREATED)


class CurrencyRateByDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        date_str = request.GET.get("date")
        if not date_str:
            return Response({"detail": _("Missing ?date=YYYY-MM-DD")}, status=400)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": _("Invalid date format.")}, status=400)

        currency = get_object_or_404(FarmCurrency, id=pk, farm=request.user.active_farm)
        try:
            rate = CurrencyRate.objects.get(farm_currency=currency, date=date)
        except CurrencyRate.DoesNotExist:
            raise NotFound(_("Rate not found for this date."))

        return Response(CurrencyRateSerializer(rate).data)
    

class CurrencyRateRangeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")

        if not from_date or not to_date:
            return Response({"detail": _("Both ?from and ?to are required.")}, status=400)

        try:
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": _("Invalid date format.")}, status=400)

        currency = get_object_or_404(FarmCurrency, id=pk, farm=request.user.active_farm)
        rates = CurrencyRate.objects.filter(
            farm_currency=currency,
            date__range=(from_date, to_date)
        ).order_by("date")

        return Response(CurrencyRateSerializer(rates, many=True).data)
