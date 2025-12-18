from django.db import models

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from sublayeritems.models import SublayerItem


class Bracket(TimeStampedModel, UniversalIdModel, ReferenceModel):
    name = models.CharField(max_length=255,)
    sublayeritem = models.ForeignKey(
        SublayerItem, on_delete=models.CASCADE, related_name="brackets"
    )

    class Meta:
        verbose_name = "Bracket"
        verbose_name_plural = "Brackets"
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "sublayeritem"],
                name="unique_bracket_name_per_sublayeritem",
            )
        ]

    def __str__(self):
        return self.name
