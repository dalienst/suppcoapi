import uuid

from cloudinary.models import CloudinaryField
from django.db import models
from accounts.utils import generate_reference


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UniversalIdModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=255,
    )

    class Meta:
        abstract = True


class AbstractProfileModel(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = CloudinaryField("profiles", blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    identification = models.CharField(max_length=20, blank=True, null=True)
    kra_pin = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class ReferenceModel(models.Model):
    reference = models.CharField(max_length=20, blank=True, null=True, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = generate_reference()
        super().save(*args, **kwargs)
