from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from companies.models import Company

User = get_user_model()


class Inventory(TimeStampedModel, UniversalIdModel, ReferenceModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="inventories"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_inventories"
    )
    name = models.CharField(max_length=800, help_text="Unique name in the company")
    inventory_code = models.CharField(
        max_length=1000,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique code for the inventory",
    )
    description = models.TextField(
        blank=True, null=True, help_text="Description of the inventory"
    )

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_inventory_name_per_company",
            )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.inventory_code:
            base_inventory_code = slugify(f"inventory-{self.company.name}-{self.name}")
            inventory_code = base_inventory_code
            count = 1
            while Inventory.objects.filter(inventory_code=inventory_code).exists():
                inventory_code = f"{base_inventory_code}-{count}"
                count += 1
            self.inventory_code = inventory_code
        super().save(*args, **kwargs)
