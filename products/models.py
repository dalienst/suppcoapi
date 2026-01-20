from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from layers.models import Layer
from sublayers.models import SubLayer
from sublayeritems.models import SublayerItem
from brackets.models import Bracket
from companies.models import Company
from branches.models import Branch
from sites.models import Site
from products.utils import generate_sku
from paymentoptions.models import PaymentOption

User = get_user_model()


class Product(TimeStampedModel, UniversalIdModel, ReferenceModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_products"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        related_name="branch_products",
        null=True,
        blank=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        related_name="site_products",
        null=True,
        blank=True,
    )
    layer = models.ForeignKey(
        Layer,
        on_delete=models.SET_NULL,
        related_name="layer_products",
        null=True,
        blank=True,
    )
    sublayer = models.ForeignKey(
        SubLayer,
        on_delete=models.SET_NULL,
        related_name="sublayer_products",
        null=True,
        blank=True,
    )
    sublayeritem = models.ForeignKey(
        SublayerItem,
        on_delete=models.SET_NULL,
        related_name="sublayeritem_products",
        null=True,
        blank=True,
    )
    bracket = models.ForeignKey(
        Bracket,
        on_delete=models.SET_NULL,
        related_name="bracket_products",
        null=True,
        blank=True,
    )
    # key fields
    source_location = models.CharField(max_length=255, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    specifications = models.JSONField(
        null=True,
        blank=True,
    )
    image = CloudinaryField("products", blank=True, null=True)
    sku = models.CharField(
        max_length=255, default=generate_sku, unique=True, editable=False
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # payment options
    payment_options = models.ManyToManyField(
        PaymentOption, related_name="products", blank=True
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name or "Unnamed Product"
