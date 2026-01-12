from django.db import models
from django.contrib.auth import get_user_model

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from inventory.models import Inventory

User = get_user_model()


class Layer(UniversalIdModel, TimeStampedModel, ReferenceModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="layers")
    name = models.CharField(
        max_length=255,
    )
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="layers"
    )

    class Meta:
        verbose_name = "Layer"
        verbose_name_plural = "Layers"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "inventory"],
                name="unique_layer_name_per_inventory",
            )
        ]

    def __str__(self):
        return self.name
