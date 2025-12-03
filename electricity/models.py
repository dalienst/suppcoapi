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

User = get_user_model()


class Electricity(TimeStampedModel, UniversalIdModel, ReferenceModel):
    bracket = models.ForeignKey(
        Bracket,
        on_delete=models.SET_NULL,
        related_name="bracket_electricity",
        blank=True,
        null=True,
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        related_name="branch_electricity",
        blank=True,
        null=True,
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_electricity"
    )
    layer = models.ForeignKey(
        Layer,
        on_delete=models.SET_NULL,
        related_name="layer_electricity",
        blank=True,
        null=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        related_name="site_electricity",
        blank=True,
        null=True,
    )
    sublayer = models.ForeignKey(
        SubLayer,
        on_delete=models.SET_NULL,
        related_name="sublayer_electricity",
        blank=True,
        null=True,
    )
    sublayeritem = models.ForeignKey(
        SublayerItem,
        on_delete=models.SET_NULL,
        related_name="sublayeritem_electricity",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="electricity")

    source_location = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    specifications = models.JSONField(blank=True, null=True)
    image = CloudinaryField("electricity", blank=True, null=True)

    class Meta:
        verbose_name = "Electricity"
        verbose_name_plural = "Electricity"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name
