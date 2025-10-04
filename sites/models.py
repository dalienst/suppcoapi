from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from companies.models import Company
from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel

User = get_user_model()


class Site(UniversalIdModel, TimeStampedModel, ReferenceModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sites")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sites")
    identity = models.CharField(max_length=700, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.identity:
            self.identity = slugify(f"site-{self.company.name}-{self.name}")
        super().save(*args, **kwargs)
