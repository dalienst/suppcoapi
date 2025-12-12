from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from accounts.abstracts import UniversalIdModel, TimeStampedModel, ReferenceModel
from companies.models import Company
from permissions.models import Permission

User = get_user_model()


class Role(UniversalIdModel, TimeStampedModel, ReferenceModel):
    name = models.CharField(max_length=2555)
    is_head = models.BooleanField(
        default=False,
        help_text="Role head: if they can be in charge of branches or sites",
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="roles")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_roles"
    )
    identity = models.CharField(max_length=100, null=True, blank=True, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        related_name="roles_permissions",
        blank=True,
    )

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["company", "-created_at"]
        unique_together = ("name", "company")

    def __str__(self):
        return f"{self.name} - {self.company.name}"

    def save(self, *args, **kwargs):
        if not self.identity:
            base_identity = slugify(f"role-{self.company.name}-{self.name}")
            identity = base_identity
            count = 1
            while Role.objects.filter(identity=identity).exists():
                identity = f"{base_identity}-{count}"
                count += 1
            self.identity = identity

        super().save(*args, **kwargs)
