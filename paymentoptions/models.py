from django.db import models
from django.contrib.auth import get_user_model

from accounts.abstracts import ReferenceModel, TimeStampedModel, UniversalIdModel


User = get_user_model()


class PaymentOption(ReferenceModel, TimeStampedModel, UniversalIdModel):
    """
    A product can have more than one payment option
    """

    PAYMENT_TYPE_CHOICES = (
        ("FIXED", "FIXED"),
        ("PAYMENT_ON_DELIVERY", "PAYMENT_ON_DELIVERY"),
        ("SPLIT_50_50", "SPLIT_50_50"),
        ("FLEXIBLE", "FLEXIBLE"),
    )
    payment_type = models.CharField(
        max_length=50,
        choices=PAYMENT_TYPE_CHOICES,
        help_text="Type of payment plan",
    )
    min_deposit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Required deposit percentage (e.g., 20.00 for 20%), mainly for Flexible",
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment_options"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Payment Option"
        verbose_name_plural = "Payment Options"
        ordering = ["-created_at"]

    @property
    def is_fixed(self):
        return self.payment_type == "FIXED"

    @property
    def is_payment_on_delivery(self):
        return self.payment_type == "PAYMENT_ON_DELIVERY"

    @property
    def is_split_50_50(self):
        return self.payment_type == "SPLIT_50_50"

    @property
    def is_flexible(self):
        return self.payment_type == "FLEXIBLE"

    def __str__(self):
        return self.name
