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


class ShellEquipment(TimeStampedModel, UniversalIdModel, ReferenceModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shell_equipment"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_shell_equipment"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        related_name="branch_shell_equipment",
        null=True,
        blank=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        related_name="site_shell_equipment",
        null=True,
        blank=True,
    )
    layer = models.ForeignKey(
        Layer,
        on_delete=models.SET_NULL,
        related_name="layer_shell_equipment",
        null=True,
        blank=True,
    )
    sublayer = models.ForeignKey(
        SubLayer,
        on_delete=models.SET_NULL,
        related_name="sublayer_shell_equipment",
        null=True,
        blank=True,
    )
    sublayeritem = models.ForeignKey(
        SublayerItem,
        on_delete=models.SET_NULL,
        related_name="sublayeritem_shell_equipment",
        null=True,
        blank=True,
    )
    bracket = models.ForeignKey(
        Bracket,
        on_delete=models.SET_NULL,
        related_name="bracket_shell_equipment",
        null=True,
        blank=True,
    )
    # key fields
    source_location = models.CharField(max_length=255, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    specifications = models.JSONField(null=True, blank=True)
    image = CloudinaryField("shell_equipment", blank=True, null=True)

    class Meta:
        verbose_name = "Shell Equipment"
        verbose_name_plural = "Shell Equipment"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name
