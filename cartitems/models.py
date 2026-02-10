from django.db import models

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from cart.models import Cart
from products.models import Product
from paymentoptions.models import PaymentOption


class CartItem(TimeStampedModel, UniversalIdModel, ReferenceModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    # Payment Preferences
    payment_option = models.ForeignKey(
        PaymentOption, on_delete=models.SET_NULL, null=True, blank=True
    )
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="User input for Flexible deposit",
    )
    duration_months = models.IntegerField(
        null=True, blank=True, help_text="User input for Flexible duration"
    )
    monthly_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="User input for Flexible monthly amount (alternative to duration)",
    )

    @property
    def sub_total(self):
        return self.product.price * self.quantity

    @property
    def payable_amount(self):
        if self.payment_option and self.payment_option.is_flexible:
            return self.deposit_amount or 0
        return self.sub_total

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in {self.cart}"
