from django.db import models
from django.contrib.auth import get_user_model

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from layers.models import Layer
from sublayers.models import SubLayer
from sublayeritems.models import SublayerItem
from brackets.models import Bracket
from companies.models import Company
from branches.models import Branch
from sites.models import Site

User = get_user_model()


class Plumbing(TimeStampedModel, UniversalIdModel, ReferenceModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="plumbing")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_plumbing"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        related_name="branch_plumbing",
        null=True,
        blank=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        related_name="site_plumbing",
        null=True,
        blank=True,
    )
    layer = models.ForeignKey(
        Layer,
        on_delete=models.SET_NULL,
        related_name="layer_plumbing",
        null=True,
        blank=True,
    )
    sublayer = models.ForeignKey(
        SubLayer,
        on_delete=models.SET_NULL,
        related_name="sublayer_plumbing",
        null=True,
        blank=True,
    )
    sublayeritem = models.ForeignKey(
        SublayerItem,
        on_delete=models.SET_NULL,
        related_name="sublayeritem_plumbing",
        null=True,
        blank=True,
    )
    bracket = models.ForeignKey(
        Bracket,
        on_delete=models.SET_NULL,
        related_name="bracket_plumbing",
        null=True,
        blank=True,
    )
    # key fields
    source_location = models.CharField(max_length=255, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    specifications = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Plumbing"
        verbose_name_plural = "Plumbing"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name
