from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel


User = get_user_model()


class Company(TimeStampedModel, UniversalIdModel, ReferenceModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=255, blank=False, null=False, unique=True)
    phone = models.CharField(null=True, blank=True, max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)
    logo = CloudinaryField("company", blank=True, null=True)
    registration_number = models.CharField(
        max_length=255, null=True, blank=True, unique=True
    )
    kra_pin = models.CharField(max_length=255, null=True, blank=True, unique=True)
    currency = models.CharField(max_length=20, blank=True, null=True)
    vat_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    fiscal_year = models.CharField(max_length=20, blank=True, null=True)
    vat_compliance = models.BooleanField(default=False)
    type = models.CharField(max_length=20, blank=True, null=True)
    identity = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """
        Set the type of company based on the type of user
        """
        if self.user.is_contractor:
            self.type = "contractor"
        elif self.user.is_supplier:
            self.type = "supplier"

        if not self.identity:
            self.identity = slugify(f"{self.user.username}-{self.type}")
        super().save(*args, **kwargs)
