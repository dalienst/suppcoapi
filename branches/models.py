from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from companies.models import Company

User = get_user_model()


class Branch(TimeStampedModel, UniversalIdModel, ReferenceModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="branches")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="branch"
    )
    identity = models.CharField(max_length=700, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.identity:
            self.identity = slugify(f"branch-{self.company.name}-{self.name}")
        super().save(*args, **kwargs)
