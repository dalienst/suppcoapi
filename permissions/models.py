from django.db import models

from accounts.abstracts import TimeStampedModel, ReferenceModel, UniversalIdModel


class Permission(ReferenceModel, UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    codename = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        ordering = ["name"]

    def __str__(self):
        return self.name
