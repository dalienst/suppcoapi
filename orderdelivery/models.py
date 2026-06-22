import random
from django.db import models
from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from delivery.models import DeliveryZone
from orders.models import Order

def generate_delivery_pin():
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


class OrderDelivery(TimeStampedModel, UniversalIdModel, ReferenceModel):
    DELIVERY_METHOD_CHOICES = (
        ("DELIVERY", "Supplier Managed Delivery"),
        ("PICKUP", "Contractor Self-Pickup"),
    )

    DELIVERY_STATUS_CHOICES = (
        ("PENDING", "Pending Dispatch"),
        ("DISPATCHED", "In Transit"),
        ("READY_FOR_PICKUP", "Ready for Pickup"),
        ("COMPLETED", "Fulfilled"),
        ("CANCELLED", "Cancelled"),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="delivery_detail",
        help_text="The supplier split order associated with this delivery detail"
    )
    delivery_method = models.CharField(
        max_length=30,
        choices=DELIVERY_METHOD_CHOICES,
        default="DELIVERY"
    )
    delivery_zone = models.ForeignKey(
        DeliveryZone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deliveries",
        help_text="Selected delivery zone (if delivery method is supplier delivery)"
    )
    shipping_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Calculated shipping fee captured at checkout"
    )
    delivery_address = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed location for delivery or pickup instructions"
    )
    recipient_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Designated contact person name for delivery/pickup"
    )
    recipient_phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text="Designated contact person phone number"
    )
    status = models.CharField(
        max_length=50,
        choices=DELIVERY_STATUS_CHOICES,
        default="PENDING"
    )
    secure_pin = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Generated secure 6-digit PIN code to verify receipt"
    )
    carrier_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name of the carrier or driver delivering the materials"
    )
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Tracking reference for carrier"
    )

    class Meta:
        verbose_name = "Order Delivery"
        verbose_name_plural = "Order Deliveries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.delivery_method} for Order {self.order.reference} - Status: {self.status}"

    def save(self, *args, **kwargs):
        if not self.secure_pin:
            self.secure_pin = generate_delivery_pin()
        super().save(*args, **kwargs)
