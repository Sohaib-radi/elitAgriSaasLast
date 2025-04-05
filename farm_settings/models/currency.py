# farm_settings/models/currency.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin
from core.models.farm import Farm
from core.models.base import FarmLinkedModel

class Currency(models.Model):
    """
    Static list of all supported currencies.
    """
    code: str = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("Currency Code"),
        help_text=_("ISO code for the currency, e.g., USD, EUR."),
        db_index=True,
    )
    name: str = models.CharField(
        max_length=100,
        verbose_name=_("Currency Name"),
        help_text=_("Full name of the currency."),
    )

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class FarmCurrency(TimeStampedModel, CreatedByMixin, FarmLinkedModel):
    """
    A currency that a specific farm has enabled in its environment.
    """
    """ farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="farm_currencies",
        verbose_name=_("Farm"),
        help_text=_("Farm to which this currency is linked."),
    ) """
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="enabled_for_farms",
        verbose_name=_("Currency"),
        help_text=_("Reference to the global currency entity."),
    )

    is_active: bool = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("If disabled, this currency won't be usable in new transactions."),
    )

    class Meta:
        unique_together = ("farm", "currency")
        verbose_name = _("Farm Currency")
        verbose_name_plural = _("Farm Currencies")

    def __str__(self) -> str:
        return f"{self.currency.code} - {self.farm.name}"

class CurrencyRate(TimeStampedModel, CreatedByMixin):
    """
    Historical exchange rate of a currency for a specific farm and date.
    """
    farm_currency = models.ForeignKey(
        FarmCurrency,
        on_delete=models.CASCADE,
        related_name="rates",
        verbose_name=_("Farm Currency"),
        help_text=_("Farm currency to which this rate belongs."),
    )

    date: models.DateField = models.DateField(
        verbose_name=_("Rate Date"),
        help_text=_("Date of the rate."),
        db_index=True,
    )

    rate: models.DecimalField = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        verbose_name=_("Exchange Rate"),
        help_text=_("Value of the currency compared to the farm's base currency."),
    )

    class Meta:
        unique_together = ("farm_currency", "date")
        verbose_name = _("Currency Rate")
        verbose_name_plural = _("Currency Rates")
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.farm_currency.currency.code} - {self.date}: {self.rate}"
