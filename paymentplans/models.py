from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from paymentoptions.models import PaymentOption
from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel

User = get_user_model()


class PaymentPlan(TimeStampedModel, UniversalIdModel, ReferenceModel):
    """
    For each product, there can be one payment plan
    - In the scenario of flexible, the contractor will have to enter
    their payment plan for the remaining amount less deposit stated in the payment option
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="payment_plan"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment_plan"
    )
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    plan = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Payment Plan"
        verbose_name_plural = "Payment Plans"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.product.product_name} - {self.payment_option.name}"
