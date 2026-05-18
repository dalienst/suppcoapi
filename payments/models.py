from django.db import models
from django.contrib.auth import get_user_model
from accounts.abstracts import ReferenceModel, TimeStampedModel, UniversalIdModel
from orders.models import Order

User = get_user_model()


class Payment(ReferenceModel, TimeStampedModel, UniversalIdModel):
    STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    orders = models.ManyToManyField(
        Order,
        blank=True,
        related_name="grouped_payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paystack_reference = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text="Transaction reference returned by Paystack",
    )
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="e.g. mpesa, card, bank",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.reference} ({self.status}) - {self.amount} KES"
