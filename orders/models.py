from django.db import models
from django.contrib.auth import get_user_model
from companies.models import Company
from products.models import Product, PaymentType
from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel

User = get_user_model()


class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "Pending (Waiting for Supplier)"
    ACCEPTED = "ACCEPTED", "Accepted (Preparing)"
    DISPATCHED = "DISPATCHED", "Dispatched"
    DELIVERED = "DELIVERED", "Delivered"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class PaymentStatus(models.TextChoices):
    UNPAID = "UNPAID", "Unpaid"
    PARTIAL = "PARTIAL", "Partially Paid"
    PAID = "PAID", "Fully Paid"
    OVERDUE = "OVERDUE", "Overdue"


class Order(TimeStampedModel, UniversalIdModel, ReferenceModel):
    # Buyer Info
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders_placed"
    )
    buyer_company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="purchases",
        null=True,
        blank=True,
    )

    # Supplier Info (An order is typically to one supplier, or system needs to split cart)
    # Assuming Order per Supplier for simplicity in this architecture
    supplier_company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="orders_received"
    )

    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID
    )

    # Payment Plan Selection
    # The buyer selects a payment type that applies to this order.
    # Note: If an order has multiple items, they usually must share the payment term,
    # or the order should be split.
    selected_payment_type = models.CharField(
        max_length=50, choices=PaymentType.choices, default=PaymentType.IMMEDIATE
    )

    # For Flexible terms: Captures the buyer's proposal or agreed details
    # e.g. { "proposed_installments": 3, "interval": "monthly" }
    payment_terms_proposal = models.JSONField(blank=True, null=True)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # Addresses (Simplified)
    delivery_address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.reference} - {self.buyer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    # Snapshot product details in case they change
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, blank=True, null=True)

    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.quantity * self.price_at_purchase
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"


class PaymentInstallment(TimeStampedModel, UniversalIdModel, ReferenceModel):
    """
    Tracks scheduled payments for Split or Flexible plans.
    Product: Split 50/50 -> 2 Installments.
    Product: Flexible -> 1 Deposit + N Installments.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="installments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)

    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    note = models.CharField(
        max_length=255, help_text="e.g., '50% Deposit', 'Installment 1/3'"
    )

    class Meta:
        verbose_name = "Payment Installment"
        verbose_name_plural = "Payment Installments"
        ordering = ["due_date"]
