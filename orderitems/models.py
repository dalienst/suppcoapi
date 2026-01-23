from django.db import models
from orders.models import Order
from products.models import Product
from paymentplans.models import PaymentPlan
from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel


class OrderItem(TimeStampedModel, UniversalIdModel, ReferenceModel):
    STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("AWAITING_DELIVERY", "AWAITING_DELIVERY"),
        ("DISPATCHED", "DISPATCHED"),
        ("DELIVERED", "DELIVERED"),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="order_items"
    )
    payment_plan = models.OneToOneField(
        PaymentPlan, on_delete=models.PROTECT, related_name="order_item"
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.product_name} in Order {self.order.reference}"

    def save(self, *args, **kwargs):
        if not self.price_at_purchase:
            self.price_at_purchase = self.product.price
        super().save(*args, **kwargs)
