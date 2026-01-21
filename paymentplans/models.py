from django.db import models

from products.models import Product
from paymentoptions.models import PaymentOption
from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel


class PaymentPlan(TimeStampedModel, UniversalIdModel, ReferenceModel):
    """
    For each product, there can be one payment plan
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
