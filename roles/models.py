from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from accounts.abstracts import UniversalIdModel, TimeStampedModel, ReferenceModel
from companies.models import Company

User = get_user_model()


class Role(UniversalIdModel, TimeStampedModel, ReferenceModel):
    name = models.CharField(max_length=255)
    is_head = models.BooleanField(default=False, help_text="Role head: if they can be in charge of branches or sites")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="roles")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_roles"
    )
    identity = models.CharField(max_length=100, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["-created_at"]
        unique_together = ("name", "company")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.identity:
            self.identity = slugify(f"role-{self.company.name}-{self.name}")
        super().save(*args, **kwargs)
