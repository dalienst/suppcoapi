from django.db import models

from accounts.abstracts import TimeStampedModel, ReferenceModel, UniversalIdModel
from sublayers.models import SubLayer


class SublayerItem(TimeStampedModel, ReferenceModel, UniversalIdModel):
    sublayer = models.ForeignKey(
        SubLayer, on_delete=models.CASCADE, related_name="sublayer_items"
    )
    name = models.CharField(
        max_length=255,
    )

    class Meta:
        verbose_name = "Sublayer Item"
        verbose_name_plural = "Sublayer Items"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "sublayer"],
                name="unique_sublayer_item_name_per_sublayer",
            )
        ]

    def __str__(self):
        return self.name
