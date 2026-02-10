from django.db import models
from django.contrib.auth import get_user_model
from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
import uuid

User = get_user_model()


class Order(TimeStampedModel, UniversalIdModel, ReferenceModel):
    STATUS_CHOICES = (
        ("DRAFT", "DRAFT"),
        ("PLACED", "PLACED"),
        ("PARTIALLY_DISPATCHED", "PARTIALLY_DISPATCHED"),
        ("DISPATCHED", "DISPATCHED"),
        ("COMPLETED", "COMPLETED"),
        ("CANCELLED", "CANCELLED"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="DRAFT")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference = models.CharField(
        max_length=100, unique=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.reference} - {self.user}"
