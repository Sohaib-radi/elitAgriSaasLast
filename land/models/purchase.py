from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from core.models.base import TimeStampedModel, CreatedByMixin
from django.contrib.auth import get_user_model


User = get_user_model()


class TransactionType(models.TextChoices):
    PURCHASE = "purchase", _("Purchase")
    SALE = "sale", _("Sale")


class LandPurchase(TimeStampedModel, CreatedByMixin):
    land = models.ForeignKey("land.Land", on_delete=models.CASCADE, related_name="purchases", verbose_name=_("Land"))
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        default=TransactionType.PURCHASE,
        verbose_name=_("Transaction Type"),
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="land_purchases",
        verbose_name=_("Buyer"),
    )
    seller_name = models.CharField(max_length=255, default="Farm Seller", verbose_name=_("Seller Name"))

    seller_contact = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Seller Contact"))
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Price (USD)"))
    purchase_date = models.DateTimeField(default=now,  verbose_name=_("Transaction Date"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Land Transaction")
        verbose_name_plural = _("Land Transactions")
        ordering = ["-purchase_date"]

    def __str__(self):
        return f"{self.get_transaction_type_display()} of {self.land.land_number}"
