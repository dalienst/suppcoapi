from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from companies.models import Company
from branches.models import Branch
from sites.models import Site

User = get_user_model()


class BuilderPlant(TimeStampedModel, UniversalIdModel, ReferenceModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="builders_plant"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="builders_plant"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="builders_plant",
        blank=True,
        null=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="builders_plant",
        blank=True,
        null=True,
    )
    source_location = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    specifications = models.JSONField(blank=True, null=True)
    image = CloudinaryField("builders_plant", blank=True, null=True)

    class Meta:
        verbose_name = "Builder Plant"
        verbose_name_plural = "Builder Plants"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product_name
