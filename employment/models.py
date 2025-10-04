from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from accounts.abstracts import UniversalIdModel, TimeStampedModel, ReferenceModel
from companies.models import Company
from roles.models import Role

User = get_user_model()


class Employment(UniversalIdModel, TimeStampedModel, ReferenceModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employment")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="employments"
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="employees")
    is_active = models.BooleanField(default=True)
    identity = models.CharField(max_length=1000, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Employment"
        verbose_name_plural = "Employments"
        ordering = ["-created_at"]
        unique_together = ("user", "company")

    def __str__(self):
        return f"{self.user} - {self.role.name} at {self.company.name}"

    def clean(self):
        if self.role.company != self.company:
            raise ValueError("Role is not in this company")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.identity:
            self.identity = slugify(
                f"employment-{self.company.name}-{self.user.username}-{self.role.name}"
            )

        if self.user.is_contractor or self.user.is_supplier:
            raise ValueError(
                "Contractors and suppliers cannot have Employment records."
            )

        super().save(*args, **kwargs)
