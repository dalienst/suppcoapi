from django.db import models
from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from companies.models import Company


class DeliveryZone(TimeStampedModel, UniversalIdModel, ReferenceModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="delivery_zones",
        help_text="Supplier company that offers delivery to this zone"
    )
    city = models.CharField(
        max_length=150,
        help_text="Target city or regional hub name (e.g. Nairobi, Mombasa, Kisumu)"
    )
    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Shipping fee for delivery to this zone"
    )
    estimated_days = models.PositiveIntegerField(
        default=2,
        help_text="Estimated time in days for delivery to arrive"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this delivery zone is currently active"
    )

    class Meta:
        verbose_name = "Delivery Zone"
        verbose_name_plural = "Delivery Zones"
        unique_together = ("company", "city")
        ordering = ["city", "-created_at"]

    def __str__(self):
        return f"{self.city} ({self.company.name}) - KES {self.fee}"
