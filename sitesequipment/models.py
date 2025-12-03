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


class SitesEquipment(TimeStampedModel, UniversalIdModel, ReferenceModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sites_equipment"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_sites_equipment"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        related_name="branch_sites_equipment",
        null=True,
        blank=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        related_name="site_sites_equipment",
        null=True,
        blank=True,
    )
    layer = models.ForeignKey(
        Layer,
        on_delete=models.SET_NULL,
        related_name="layer_sites_equipment",
        null=True,
        blank=True,
    )
    sublayer = models.ForeignKey(
        SubLayer,
        on_delete=models.SET_NULL,
        related_name="sublayer_sites_equipment",
        null=True,
        blank=True,
    )
    sublayeritem = models.ForeignKey(
        SublayerItem,
        on_delete=models.SET_NULL,
        related_name="sublayeritem_sites_equipment",
        null=True,
        blank=True,
    )
    bracket = models.ForeignKey(
        Bracket,
        on_delete=models.SET_NULL,
        related_name="bracket_sites_equipment",
        null=True,
        blank=True,
    )
    # key fields
    source_location = models.CharField(max_length=255, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    specifications = models.JSONField(null=True, blank=True)
    image = CloudinaryField("site_equipment", blank=True, null=True)

    class Meta:
        verbose_name = "Site Equipment"
        verbose_name_plural = "Site Equipment"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name
